from profilerApp import db

class userTable(db.Model):
    uniqueTableName = db.Column(db.String(80), primary_key=True, nullable=False)
    connectionId = db.Column(db.String(80), nullable=False)
    schema = db.Column(db.String(80),nullable=False)
    table = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"connectionId('{self.connectionId}'"

    def to_dict(self):
        dbConncetionsDict =  {
            "uniqueTableName": self.uniqueTableName,    
            "connectionId": self.connectionId,
            "schema": self.schema,
            "table": self.table,
        }
        return dbConncetionsDict