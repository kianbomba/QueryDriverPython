
class SQLException(Exception):
    def __init__(self, sql: str, parameters: list, message: str = ""):
        if len(message) == 0:
            message = "Something is wrong with the sql or database connection"

        super(SQLException, self).__init__(message)
        self._sql = sql
        self._parameters = parameters

    @property
    def sql(self) -> str:
        return self._sql

    @property
    def parameters(self) -> list:
        return self._parameters
