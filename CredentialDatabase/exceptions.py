from psycopg2 import Error


class DBConnectorError(ConnectionError):
    """DBConnectorException"""
    pass


class DBCreatorError(Exception):
    """DBCreatorException"""
    pass


class DBInserterError(Exception):
    """DBInserterException"""
    pass


class DBIntegrityError(Exception):
    """DBIntegrityError"""
    pass
