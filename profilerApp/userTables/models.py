from profilerApp import db

class userTable(db.Model):
    connectionId = db.Column(db.String(80), nullable=False)
    schema = db.Column(db.String(80), primary_key=True, nullable=False)
    table = db.Column(db.String(80), primary_key=True, nullable=False)

    def __repr__(self):
        return f"connectionID('{self.connectionId}'"

    def to_dict(self):
        dbConncetionsDict =  {
            "connectionID": self.connectionId,
            "schema": self.schema,
            "table": self.table,
        }
        return dbConncetionsDict