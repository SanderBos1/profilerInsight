from src.config import SingletonDB
from src.config import SingletonFernet

DB = SingletonDB.get_instance()

class DbConnections(DB.Model):
    """
    Represents a database connection configuration.

    This class is an SQLAlchemy model that defines the schema for storing database connection
    details, including encrypted passwords. It provides methods for password encryption/decryption
    and converting the model to a dictionary.

    Attributes:
        connection_id (str): Unique identifier for the connection.
        host (str): Hostname or IP address of the database server.
        port (Int): Port number used for the connection.
        username (str): Username for the database connection.
        _password (bytes): Encrypted password for the database connection.
        database (str): Name of the database.
        db_type (str): Type of the database.
        extra_info (str): Additional information about the database connection
    """

    connection_id = DB.Column(DB.String(80), primary_key=True, unique=True, nullable=False)
    server = DB.Column(DB.String(80), unique=False, nullable=False)
    port = DB.Column(DB.Integer, unique=False, nullable=False)
    username = DB.Column(DB.String(80), unique=False, nullable=False)
    _password = DB.Column(DB.LargeBinary, nullable=False)
    database = DB.Column(DB.String(120), unique=False, nullable=False)
    db_type = DB.Column(DB.String(80), unique=False, nullable=False)
    extra_info = DB.Column(DB.String(500), unique=False, nullable=True)

    def __repr__(self):
        """
        Return a string representation of the DbConnections instance.

        The string representation includes the connection_id.

        Returns:
            str: A string representation of the DbConnections instance.
        """
        return f"DbConnections(connection_id='{self.connection_id}')"
    
    @property
    def password(self):
        """
        Decrypt and retrieves the password for the database connection.

        Uses the cipher suite to decrypt the stored encrypted password.

        Returns:
            str: The decrypted password as a string.
        """
        cipher_suite = SingletonFernet.get_instance()
        return cipher_suite.decrypt(self._password).decode('utf-8')

    @password.setter
    def password(self, raw_password):
        """
        Encrypt and sets the password for the database connection.

        Uses the cipher suite to encrypt the provided raw password and store it.

        Args:
            raw_password (str): The plaintext password to be encrypted.
        """
        cipher_suite = SingletonFernet.get_instance()
        self._password = cipher_suite.encrypt(raw_password.encode('utf-8'))

    def to_dict(self):
        """
        Convert the DbConnections instance to a dictionary representation.

        The dictionary includes all attributes of the instance except the encrypted password.

        Returns:
            dict: A dictionary representation of the DbConnections instance.
        """
        db_connection_dict = {
            "connection_id": self.connection_id,
            "server": self.server,
            "port": self.port,
            "username": self.username,
            "database": self.database,
            "db_type": self.db_type,
            "extra_info": self.extra_info
        }
        return db_connection_dict
