class ResultSet(object):
    """
        :parameter sql              => this would be easier for debugging later on if needed
        :parameter parameters       => this would be easier for debugging later on if needed
    """
    def __init__(self, sql: str, parameters: list,):
        self._sql = sql
        self._rowcount = 0
        self._inserted_id = 0
        self._parameters = parameters
        self._affected_rows = 0
        self._data = []

    def set_data(self, data: list):
        self._data = data
        return self

    def set_row_count(self, row_count: int):
        self._rowcount = row_count
        return self

    def executed_sql(self) -> str:
        return self._sql

    def data(self) -> list:
        return self._data

    def row_count(self) -> int:
        return self._rowcount

    def last_inserted_id(self) -> int:
        return self._inserted_id

    def set_inserted_id(self, inserted_id: int):
        self._inserted_id = inserted_id
        return self

    def set_affected_rows(self, affected_rows: int):
        self._affected_rows = affected_rows
        return self

    def affected_rows(self) -> int:
        return self._affected_rows
