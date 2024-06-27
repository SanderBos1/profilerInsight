from profilerApp import db

class dbConncetions(db.Model):
    connectionID = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    Host = db.Column(db.String(80), unique=False, nullable=False)
    Port = db.Column(db.String(80), unique=False, nullable=False)
    UserName = db.Column(db.String(80), unique=False, nullable=False)
    Password = db.Column(db.String(500), unique=False, nullable=False)
    DataBase = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"connectionID('{self.connectionID}'"

    def to_dict(self):
        dbConncetionsDict =  {
            "connectionID": self.connectionID,
            "host": self.Host,
            "port": self.Port,
            "username": self.UserName,
            "password": self.Password,
            "database": self.DataBase,
        }
        return dbConncetionsDict