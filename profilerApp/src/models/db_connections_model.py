from src import db
from src.config.encryption import EncryptionUtil  # Import the encryption utility
import os



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
        cipher_suite = EncryptionUtil.get_cipher_suite()
        return cipher_suite.decrypt(self._password).decode('utf-8')

    @password.setter
    def password(self, raw_password):
        cipher_suite = EncryptionUtil.get_cipher_suite()
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


