from ..userTables import userTable
from ..userConnections import dbConncetions
from .models import ingestionOverview
from profilerApp import db
from ..database_query_manager import DatabaseQueryManager
from psycopg2 import sql

class Profiler:

    def __init__(self, tableName, columnName):
        """
        Initializes the Profiler with the specified table and column names.

        Args:
            table_name (str): The name of the table to be profiled.
            column_name (str): The name of the column to be profiled.
        """
        self.tableName = tableName
        self.columnName = columnName

    def checkExisting(self):
        """
        Checks if a record for the given table and column already exists in the ingestionOverview table.

        Returns:
            bool: True if the record exists, False otherwise.
        """
        return ingestionOverview.query.filter_by(Table=self.tableName, Column=self.columnName).first() is not None
    
    def getOverviewLocal(self):
        """
        Retrieves the profiling overview for the given table and column from the local database.

        Returns:
            dict: A dictionary containing the row count, distinct values count, NaN values count, and column type.
            If no record is found, an empty dictionary is returned.
        """
        existing_record = ingestionOverview.query.filter_by(Table=self.tableName, Column=self.columnName).first()
        if existing_record:
            return {
                "rowCount": existing_record.numberRows,
                "distinctValues": existing_record.numberUnique,
                "nanValues": existing_record.numberNans,
                "columnType": existing_record.columnType
            }
        return {}

    def ingestData(self):
        """
        Ingests and profiles data for the specified table and column, updating the local ingestionOverview table.

        This method executes queries to count rows, distinct values, NaN values, and determine the column type.
        The results are then inserted into or updated in the ingestionOverview table.

        Returns:
            dict: A dictionary containing the row count, distinct values count, NaN values count, and column type.
        
        Raises:
            ValueError: If the user table or connection cannot be found.
            RuntimeError: If there is an error executing any of the queries.
        """
        userTableValues = userTable.query.filter(userTable.uniqueTableName==self.tableName).first()
        if not userTableValues:
            raise ValueError(f"No user table found with uniqueTableName '{self.table_name}'")
        connection = dbConncetions.query.filter_by(connectionId=userTableValues.connectionId).first()   
        if not connection:
            raise ValueError(f"No connection found with connectionId '{userTableValues.connectionId}'")
        userDatabaseConnection = DatabaseQueryManager("postgresql", connection)

        rowQuery = sql.SQL("SELECT COUNT(*) FROM {}.{}").format(
            sql.Identifier(userTableValues.schema),
            sql.Identifier(userTableValues.table)
        )
        rowCount = userDatabaseConnection.executeQuery(rowQuery)

        distinctValuesQuery = sql.SQL("SELECT COUNT(DISTINCT %s) FROM {}.{}").format(
            sql.Identifier(userTableValues.schema),
            sql.Identifier(userTableValues.table)
        )
        distinctValues = userDatabaseConnection.executeQuery(distinctValuesQuery,  params=(self.columnName,))

        nanValuesQuery = sql.SQL("SELECT COUNT(*) FROM {}.{} WHERE %s IS NULL").format(
            sql.Identifier(userTableValues.schema),
            sql.Identifier(userTableValues.table)
        )
        nanValues = userDatabaseConnection.executeQuery(nanValuesQuery,  params=(self.columnName,))

        columnType = userDatabaseConnection.executeQuery(f"SELECT data_type FROM information_schema.columns where table_name = %s AND column_name = %s", params=(userTableValues.table, self.columnName))
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