import mysql.connector
from mysql.connector.cursor_cext import MySQLCursorAbstract
import json
import pathlib
from Core.ResultSet import ResultSet
from Exception.SQLException import SQLException
from Core.SQLGenerator import SQLGenerator


class Connection(object):
    SELECT = 1
    UPDATE = 2
    INSERT = 3

    def __init__(self, config_file: str, load: bool=False, best_practice: bool=True):
        self._file = config_file
        self._config = None
        self._connection = None
        self._best_practice = best_practice

        # if we are specified to load straight away,
        # the json file would be loaded to this class
        if load:
            self.__load__()

    """
        loading the config to cache, 
        so then the configuration is able to be used for connection with database
        
        :raise Exception
    """
    def __load__(self):
        file = pathlib.Path(self._file)
        if not file.is_file():
            raise Exception("The config file is not exist")
        else:
            f = open(self._file)
            try:
                self._config = json.load(f)
            finally:
                f.close()

    """
        if the connection is None
        or actually if the connection is not open, 
        then re-establish(or establish) a new connection link to the database
    """
    def connect(self):
        if (self._config is not None and self._connection is None) or not self._connection.is_connected():
            self._connection = mysql.connector.connect(
                                                        user=self._config['username'],
                                                        password=self._config['password'],
                                                        host=self._config['host'],
                                                        database=self._config['dbname'],
                                                        port=self._config['port']
            )
    """
        :return None
        closing connection or cursor
    """
    def close(self, cursor: MySQLCursorAbstract=None):
        if cursor is not None:
            cursor.reset()
            cursor.close()

        if self._connection is not None and not self._connection.is_connected:
            self._connection.close()

    """
        :return the list of (dictionaries) all the possibilities result of the query
    """
    def fetchall(self, sql: str, params: list=[]) -> list:
        rs = self.execute_query(sql, params)
        return rs.data()

    """
        :return the last inserted id for us
    """
    def insert(self, table: str, data: dict) -> int:
        query = SQLGenerator.generate_sql_insert(table, data)
        rs = self.execute_query(query['sql'], query['parameters'], self.INSERT)
        return rs.last_inserted_id()

    """
        :return the affected rows that got updated after
    """
    def update(self, table: str, data: dict, identifiers: dict) -> int:
        query = SQLGenerator.generate_sql_update(table, data, identifiers)
        rs = self.execute_query(sql=query['sql'],
                                parameters=query['parameters'],
                                mode=self.UPDATE)

        return rs.affected_rows()

    """
        :return dictionary of the row,
        we are only fetching for one item, if there is no limit within the sql, set it
    """
    def fetchassoc(self, sql: str, params: list=[]) -> dict:
        if "LIMIT" not in sql:
            sql += " LIMIT 1"

        rs = self.execute_query(sql, params, self.SELECT)
        data = rs.data()

        if rs.row_count() > 0:
            return data[0]
        else:
            return {}

    """
        :raise {SQLException}
    """
    def execute_query(self, sql: str, parameters: list, mode: int = SELECT) -> ResultSet:
        cursor = None
        try:
            self.connect()
            cursor = self._connection.cursor(dictionary=True, buffered=True)
            cursor.execute(sql, parameters)
            rs = ResultSet(sql, parameters)

            if mode == self.INSERT:
                self._connection.commit()
                rs.set_inserted_id(cursor.lastrowid)
            elif mode == self.UPDATE:
                self._connection.commit()
                rs.set_affected_rows(cursor.rowcount)
            else:
                rs.set_data(cursor.fetchall())
                rs.set_row_count(cursor.rowcount)

            return rs
        except Exception as pe:
            raise SQLException(sql, parameters) from pe
        finally:
            if self._best_practice:
                self.close(cursor)
