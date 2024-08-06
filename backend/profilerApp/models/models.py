from profilerApp import db, cipher_suite

"""
Defines the database models for managing database connections, tables, and ingestion overview.

The `dbConnections` class manages the details of a database connection, including encrypted password storage.
The `connectedTables` class represents tables that are connected to a specific database connection.
The `ingestionOverview` class provides an overview of the ingestion details for a particular table and column.
"""


class dbConnections(db.Model):
    """
    Represents a database connection configuration.

    Attributes:
        connection_id (str): Unique identifier for the connection.
        host (str): Hostname or IP address of the database server.
        port (str): Port number used for the connection.
        username (str): Username for the database connection.
        _password (bytes): Encrypted password for the database connection.
        database (str): Name of the database.

    Methods:
        password: Decrypts and retrieves the password.
        password (setter): Encrypts and sets the password.
        to_dict: Converts the model instance to a dictionary.
    """
    connection_id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    host = db.Column(db.String(80), unique=False, nullable=False)
    port = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    _password = db.Column(db.LargeBinary, nullable=False)
    database = db.Column(db.String(120), unique=False, nullable=False)
    db_type = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return f"connection_id('{self.connection_id}'"
    
    @property
    def password(self):
        return cipher_suite.decrypt(self._password).decode('utf-8')

    @password.setter
    def password(self, raw_password):
        self._password = cipher_suite.encrypt(raw_password.encode('utf-8'))

    def to_dict(self):
        db_connection_dict =  {
            "connection_id": self.connection_id,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "database": self.database,
            "db_type": self.db_type
        }
        return db_connection_dict

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

class ingestionOverview(db.Model):
    """
    Provides an overview of the ingestion details for a particular table and column.

    Attributes:
        table (str): Name of the table.
        column (str): Name of the column.
        table_id (int): Unique identifier for the table.
        connection_id (str): Identifier of the associated database connection.
        column_length (int): Length of the column.
        column_type (str): Data type of the column.
        data_preview (str): Preview of the first 10 elements of the column.
        median_value (float): Median value of the column.
        mean_value (float): Mean value of the column.
        min_value (float): Minimum value of the column.
        max_value (float): Maximum value of the column.
        number_nans (int): Number of NaN values in the column.
        number_unique (int): Number of unique values in the column.
        number_distinct (int): Number of distinct values in the column.
        patterns (str): Patterns found in the column.
        histogram (str): Base64-encoded histogram image of the column.
        boxplot (str): Base64-encoded boxplot image of the column.

    Methods:
        __repr__: Represents the ingestion overview instance as a string.
        
    """
    table = db.Column(db.String(80),  nullable=False)
    column = db.Column(db.String(80), nullable=False)
    table_id = db.Column(db.Integer, nullable=False)
    connection_id = db.Column(db.String(80), nullable=False)
    column_length = db.Column(db.Integer, nullable=False)
    column_type = db.Column(db.String(80), nullable=False)
    data_preview = db.Column(db.Text, nullable=True)
    median_value = db.Column(db.Float, nullable=False)
    mean_value = db.Column(db.Float, nullable=False)
    min_value = db.Column(db.Float, nullable=False)
    max_value = db.Column(db.Float, nullable=False)
    number_nans = db.Column(db.Integer, nullable=False)
    number_unique = db.Column(db.Integer, nullable=False) 
    number_distinct= db.Column(db.Integer, nullable=False)
    patterns = db.Column(db.String(80), nullable=True)
    histogram = db.Column(db.Text, nullable=True)
    boxplot = db.Column(db.Text, nullable=True)


    __table_args__ = (
        db.PrimaryKeyConstraint(
            table, column,
            ),
        )
    def __repr__(self):

        return f"Table('{self.table}', Column('{self.column}')"
