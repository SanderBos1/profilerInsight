"""
This module defines the `ConnectedTables` model for representing tables connected to specific
database connections.

The `ConnectedTables` class is an SQLAlchemy model that provides a structure for storing information
about tables that are linked to particular database connections. It includes methods for converting
model instances to dictionaries for easier serialization and manipulation.

Dependencies:
- `get_database`: A function to retrieve the SQLAlchemy database instance.

Classes:
- `ConnectedTables`: SQLAlchemy model class representing a table connected to a database.

Attributes:
- `table_id`: Unique identifier for the table entry.
- `connection_id`: Identifier of the associated database connection.
- `schemaName`: Schema name in the database.
- `tableName`: Name of the table.

Methods:
- `to_dict()`: Converts the model instance to a dictionary representation.
"""

from src.config import get_database

db = get_database()

class ConnectedTables(db.Model):
    """
    Represents a table that is connected to a specific database connection.

    This class is an SQLAlchemy model that defines the schema for storing information about tables
    associated with particular database connections.

    Attributes:
        table_id (int): Unique identifier for the table entry.
        connection_id (str): Identifier of the associated database connection.
        schemaName (str): Schema name in the database.
        tableName (str): Name of the table.

    Methods:
        to_dict: Converts the model instance to a dictionary.
    """
    table_id = db.Column(db.Integer, primary_key=True)
    connection_id = db.Column(db.String(80), nullable=False)
    schemaName = db.Column(db.String(80), nullable=False)
    tableName = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the ConnectedTables instance.

        The string representation includes the connection_id, schemaName, and tableName.

        Returns:
            str: A string representation of the ConnectedTables instance.
        """
        return f"ConnectedTables(connection_id='{self.connection_id}', \
            schemaName='{self.schemaName}', tableName='{self.tableName}')"
    
    def to_dict(self):
        """
        Converts the ConnectedTables instance to a dictionary representation.

        The dictionary includes all attributes of the instance.

        Returns:
            dict: A dictionary representation of the ConnectedTables instance.
        """
        connected_tables_dict = {
            "table_id": self.table_id,
            "connection_id": self.connection_id,
            "schemaName": self.schemaName,
            "tableName": self.tableName,
        }
        return connected_tables_dict
