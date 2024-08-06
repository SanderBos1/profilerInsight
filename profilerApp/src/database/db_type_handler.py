from ..database import PostgresConnector


CONNECTION_CLASSES = {
    'postgres': PostgresConnector,
}

def get_database_connection(db_type:str, connection:object, password:str) -> object:
    """
    Retrieves a database connection object based on the specified database type.

    This function uses the `db_type` to look up the appropriate connection class from
    the `CONNECTION_CLASSES` dictionary. It then creates an instance of that connection
    class using the provided `connection` object and `password`.

    Args:
    - db_type (str): The type of the database for which a connection object is required.
                     Supported values are defined in the `CONNECTION_CLASSES` dictionary.
    - connection (object): An object containing connection details, which is passed to
                            the connection class constructor.
    - password (str): The password required to establish the connection.

    Returns:
    - object: An instance of the database connection class corresponding to `db_type`.

    Raises:
    - ValueError: If the `db_type` is not supported or not found in `CONNECTION_CLASSES`.
    """
    connection_class = CONNECTION_CLASSES.get(db_type)
    if connection_class is None:
        raise ValueError(f"Unsupported database type: {db_type}")
    return connection_class(connection, password)