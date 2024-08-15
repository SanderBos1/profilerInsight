from src.config import SingletonDB

DB = SingletonDB.get_instance()

class ConnectedTables(DB.Model):
    """
    Represent a table that is connected to a specific database connection.

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
    db_name = DB.Column(DB.String(80), nullable=False)
    table_id = DB.Column(DB.Integer, primary_key=True)
    connection_id = DB.Column(DB.String(80), nullable=False)
    schemaName = DB.Column(DB.String(80), nullable=False)
    tableName = DB.Column(DB.String(80), nullable=False)

    def __repr__(self):
        """
        Return a string representation of the ConnectedTables instance.

        The string representation includes the connection_id, schemaName, and tableName.

        Returns:
            str: A string representation of the ConnectedTables instance.
        """
        return f"ConnectedTables(connection_id='{self.connection_id}', \
            schemaName='{self.schemaName}', tableName='{self.tableName}')"
    
    def to_dict(self):
        """
        Convert the ConnectedTables instance to a dictionary representation.

        The dictionary includes all attributes of the instance.

        Returns:
            dict: A dictionary representation of the ConnectedTables instance.
        """
        connected_tables_dict = {
            "db_name": self.db_name,
            "table_id": self.table_id,
            "connection_id": self.connection_id,
            "schemaName": self.schemaName,
            "tableName": self.tableName,
        }
        return connected_tables_dict
