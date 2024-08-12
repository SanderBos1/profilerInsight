"""
This module provides functionality for retrieving database connection objects based on 
the specified database type. It supports multiple types of database connectors and 
creates instances of the appropriate connection classes using provided connection details 
and passwords.

Key Components:
- `CONNECTION_CLASSES`: A dictionary mapping database types to their corresponding 
  connection classes.
- `get_database_connection`: A function that creates and returns an instance of a 
  database connection class based on the specified `db_type`.

Usage:
    To retrieve a database connection object:
    - Define the appropriate connection class in `CONNECTION_CLASSES`.
    - Use `get_database_connection(db_type, connection, password)` to get an instance 
      of the desired connection class.

Supported Database Types:
    - 'postgres': Maps to the `PostgresConnector` class from the `database` module.
"""

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
