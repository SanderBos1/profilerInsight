"""
This module defines the `DbConnections` model for representing database connection configurations.

It includes methods for handling encrypted passwords 
and converting the model instance to a dictionary.

Dependencies:
- `get_database`: A function to retrieve the SQLAlchemy database instance.
- `get_cipher_suite`: A function to get the cipher suite for encryption and decryption of passwords.

Classes:
- `DbConnections`: SQLAlchemy model class representing database connection configurations.

Attributes:
- `connection_id`: Unique identifier for the connection.
- `host`: Hostname or IP address of the database server.
- `port`: Port number used for the connection.
- `username`: Username for the database connection.
- `_password`: Encrypted password for the database connection.
- `database`: Name of the database.
- `db_type`: Type of the database (e.g., PostgreSQL, MySQL).

Methods:
- `password`: Property to decrypt and retrieve the password.
- `password (setter)`: Setter to encrypt and set the password.
- `to_dict()`: Converts the model instance to a dictionary representation.
"""

from src.config import get_database
from src.config import get_cipher_suite

db = get_database()

class DbConnections(db.Model):
    """
    Represents a database connection configuration.

    This class is an SQLAlchemy model that defines the schema for storing database connection
    details, including encrypted passwords. It provides methods for password encryption/decryption
    and converting the model to a dictionary.

    Attributes:
        connection_id (str): Unique identifier for the connection.
        host (str): Hostname or IP address of the database server.
        port (str): Port number used for the connection.
        username (str): Username for the database connection.
        _password (bytes): Encrypted password for the database connection.
        database (str): Name of the database.
        db_type (str): Type of the database.
    """
    connection_id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    host = db.Column(db.String(80), unique=False, nullable=False)
    port = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    _password = db.Column(db.LargeBinary, nullable=False)
    database = db.Column(db.String(120), unique=False, nullable=False)
    db_type = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the DbConnections instance.

        The string representation includes the connection_id.

        Returns:
            str: A string representation of the DbConnections instance.
        """
        return f"DbConnections(connection_id='{self.connection_id}')"
    
    @property
    def password(self):
        """
        Decrypts and retrieves the password for the database connection.

        Uses the cipher suite to decrypt the stored encrypted password.

        Returns:
            str: The decrypted password as a string.
        """
        cipher_suite = get_cipher_suite()
        return cipher_suite.decrypt(self._password).decode('utf-8')

    @password.setter
    def password(self, raw_password):
        """
        Encrypts and sets the password for the database connection.

        Uses the cipher suite to encrypt the provided raw password and store it.

        Args:
            raw_password (str): The plaintext password to be encrypted.
        """
        cipher_suite = get_cipher_suite()
        self._password = cipher_suite.encrypt(raw_password.encode('utf-8'))

    def to_dict(self):
        """
        Converts the DbConnections instance to a dictionary representation.

        The dictionary includes all attributes of the instance except the encrypted password.

        Returns:
            dict: A dictionary representation of the DbConnections instance.
        """
        db_connection_dict = {
            "connection_id": self.connection_id,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "database": self.database,
            "db_type": self.db_type
        }
        return db_connection_dict
