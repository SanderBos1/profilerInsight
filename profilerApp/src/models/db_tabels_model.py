from src import db


class connectedTables(db.Model):
    """
    Represents a table that is connected to a specific database connection.

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
        return f"connection('{self.connection_id}', schema('{self.schemaName}', table('{self.tableName}')"
    
    
    def to_dict(self):
        connected_tables_dict =  {
            "table_id": self.table_id,
            "connection_id": self.connection_id,
            "schemaName": self.schemaName,
            "tableName": self.tableName,
        }
        return connected_tables_dict
