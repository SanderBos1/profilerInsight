from profilerApp import db, cipher_suite

"""
    defines the database model of a connection
    _password means that the variable password is private and not accesable
    the @property (when we access the password proeprty) and @password.setter (when the password is set) are used to encrypt and decrypt the password
"""

class dbConncetions(db.Model):
    connectionId = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    host = db.Column(db.String(80), unique=False, nullable=False)
    port = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    _password = db.Column(db.LargeBinary, nullable=False)
    database = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"connectionId('{self.connectionId}'"
    
    @property
    def password(self):
        return cipher_suite.decrypt(self._password).decode('utf-8')

    @password.setter
    def password(self, raw_password):
        self._password = cipher_suite.encrypt(raw_password.encode('utf-8'))

    def to_dict(self):
        dbConncetionsDict =  {
            "connectionId": self.connectionId,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "database": self.database,
        }
        return dbConncetionsDict