from profilerApp import db

class dbConncetions(db.Model):
    connectionId = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    host = db.Column(db.String(80), unique=False, nullable=False)
    port = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(500), unique=False, nullable=False)
    database = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"connectionId('{self.connectionId}'"

    def to_dict(self):
        dbConncetionsDict =  {
            "connectionId": self.connectionId,
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "database": self.database,
        }
        return dbConncetionsDict