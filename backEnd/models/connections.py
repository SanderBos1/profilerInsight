from models.initializeDB import db
import json 

class dbConncetions(db.Model):
    connectionID = db.Column(db.Integer, primary_key=True)
    Host = db.Column(db.String(80), unique=False, nullable=False)
    Port = db.Column(db.String(80), unique=False, nullable=False)
    DataBase = db.Column(db.String(120), unique=False, nullable=False)
    UserName = db.Column(db.String(80), unique=False, nullable=False)
    Password = db.Column(db.String(80), unique=False, nullable=False)
    DatabaseType = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):

        dbConncetionsDict =  {
            "Host": self.Host,
            "Port": self.Port,
            "DataBase": self.DataBase,
            "UserName": self.UserName,
            "Password": self.Password,
            "DatabaseType": self.DatabaseType   
        }
        representation = json.dumps(dbConncetionsDict)
        return representation
    
    def to_dict(self):
        dbConncetionsDict =  {
            "Host": self.Host,
            "Port": self.Port,
            "DataBase": self.DataBase,
            "UserName": self.UserName,
            "Password": self.Password,
            "DatabaseType": self.DatabaseType   
        }
        return dbConncetionsDict