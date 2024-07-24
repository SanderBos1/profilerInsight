from ..userTables import userTable
from ..userConnections import dbConncetions
from ..userConnections import postgresqlConnection
from .models import ingestionOverview
from profilerApp import db

class Profiler:

    def __init__(self, tableName, columnName):
        self.tableName =tableName
        self.columnName = columnName

    def checkExisting(self):
        existing_record = ingestionOverview.query.filter_by(Table=self.tableName, Column=self.columnName).first()
        if existing_record:
            return True
        else:
            return False
    
    def getOverviewLocal(self):
        existing_record = ingestionOverview.query.filter_by(Table=self.tableName, Column=self.columnName).first()
        answer = {
            "rowCount": existing_record.numberRows,
            "distinctValues": existing_record.numberUnique, 
            "nanValues": existing_record.numberNans,
            "columnType": existing_record.columnType
        }
        return answer

    def ingestData(self):

        userTableValues = userTable.query.filter(userTable.uniqueTableName==self.tableName).first()
        connection = dbConncetions.query.filter_by(connectionId=userTableValues.connectionId).first()   
        userDatabaseConnection = postgresqlConnection(connection.host, connection.port, connection.username, connection.password, connection.database)

        rowCount = userDatabaseConnection.queryDB(f"select count(*) from {userTableValues.schema}.{ userTableValues.table}")
        distinctValues = userDatabaseConnection.queryDB(f"SELECT COUNT(DISTINCT '{self.columnName}')FROM {userTableValues.schema}.{userTableValues.table}")
        nanValues = userDatabaseConnection.queryDB(f"SELECT COUNT(*) FROM {userTableValues.schema}.{userTableValues.table} WHERE '{self.columnName}' IS NULL")
        columnType = userDatabaseConnection.queryDB(f"SELECT data_type FROM information_schema.columns where table_name = '{userTableValues.table}' AND column_name = '{self.columnName}'")
        existing_record = ingestionOverview.query.filter_by(Table=self.tableName, Column=self.columnName).first()

        if existing_record:
            existing_record.numberRows = rowCount[0][0]
            existing_record.numberNans = nanValues[0][0]
            existing_record.numberUnique = distinctValues[0][0]
            existing_record.columnType = columnType[0][0] 
        else:
            new_ingestion = ingestionOverview(Table=self.tableName, Column=self.columnName,
                                          numberRows=rowCount[0][0], numberNans=nanValues[0][0],
                                          numberUnique=distinctValues[0][0], columnType=columnType[0][0] )
            db.session.add(new_ingestion)

        db.session.commit()

        answer = {
            "rowCount": rowCount[0][0],
            "distinctValues": distinctValues[0][0], 
            "nanValues": nanValues[0][0],
            "columnType": columnType[0][0]
        }
        return answer