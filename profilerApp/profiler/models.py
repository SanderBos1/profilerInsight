from profilerApp import db


class ingestionOverview(db.Model):
    Table = db.Column(db.String(80),  nullable=False)
    Column = db.Column(db.String(80), nullable=False)
    numberRows = db.Column(db.Integer, nullable=False)
    numberNans = db.Column(db.Integer, nullable=False)
    numberUnique = db.Column(db.Integer, nullable=False) 
    columnType = db.Column(db.String(80), nullable=False)
    
    __table_args__ = (
        db.PrimaryKeyConstraint(
            Table, Column,
            ),
        )
    def __repr__(self):

        return f"Table('{self.Table}', Column('{self.Column}')"
