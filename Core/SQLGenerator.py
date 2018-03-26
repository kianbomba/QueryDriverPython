class SQLGenerator(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_sql_insert(table: str, parameters: dict) -> dict:
        sql = "INSERT INTO `{}` ".format(table)
        fields = ""
        values = ""
        params = []
        for key in parameters:
            if len(fields) == 0:
                fields += ""
            else:
                fields += ", "

            fields += "`{}`".format(key)

            if len(values) == 0:
                values += ""
            else:
                values += ","
            values += " {}".format("%s")
            params.append(parameters[key])

        sql += " ({fields}) VALUE({value})".format(fields=fields, value=values)

        return {
            'sql': sql,
            'parameters': params
        }

    @staticmethod
    def generate_sql_update(table: str, data: dict, identifiers: dict) -> dict:
        sql = "UPDATE `{}`".format(table)

        update = ""
        where_clause = ""

        parameters = []
        for key in data:
            if len(update) == 0:
                update += ""
            else:
                update += ", "

            update += "{}='%s'".format(key)
            parameters.append(data[key])

        for key in identifiers:
            if len(where_clause) == 0:
                where_clause += ""
            else:
                where_clause += " AND"
            where_clause += " `{}`='%s'".format(key)
            parameters.append(identifiers[key])

        return {
            'sql': sql,
            'parameters': parameters
        }
