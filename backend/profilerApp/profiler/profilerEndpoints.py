from flask import Blueprint, jsonify, session
from ..userTables import userTable
from ..userConnections import dbConncetions
from ..database_query_manager import DatabaseQueryManager
from .profiler import Profiler

profilerBP = Blueprint(
    "profilerBP",
    __name__,
)

"""
    input: A JSOn object with the following structure:
        tableName: str
    Goal: get the number of rows of the selected table using connectionId to find the connection information stored in the database
    output: a JSON object with the following structure:
        rowCount: int
    status codes:
        200: an Overview object could be returned
        400: the input JSON object is not valid
        500: an error occurred while adding the connection to the database
    
"""
@profilerBP.route('/getColumns/<tableName>', methods=['GET'])
def getColumns(tableName):
    try:
        userTableValues = userTable.query.filter(userTable.uniqueTableName==tableName).first()
        connection = dbConncetions.query.filter_by(connectionId=userTableValues.connectionId).first()   
        userDatabaseConnection = DatabaseQueryManager("postgresql", connection)
        query = 'SELECT table_name, column_name, data_type FROM information_schema.columns where table_name = %s ORDER BY table_name, ordinal_position;'
        params=(userTableValues.table,)
        columns = userDatabaseConnection.executeQuery(query, params)
        columnNames = []
        for tuple in columns:
            columnNames.append(tuple[1])

        answer = {
            "columnNames": columnNames,
        }
        return jsonify(answer), 200
    except Exception as e:
        return jsonify(str(e)), 500
    

@profilerBP.route('/ingest/<tableName>/<columnName>', methods=['GET'])
def ingest(tableName, columnName):
    try:
        profilerInstance = Profiler(tableName, columnName)  
        answer = profilerInstance.ingestData()
        return jsonify(answer), 200
    except Exception as e:
        return jsonify(str(e)), 500


@profilerBP.route('/getOverview/<tableName>/<columnName>', methods=['GET'])
def getOverview(tableName, columnName):
    try:
        profilerInstance = Profiler(tableName, columnName)  
        existing = profilerInstance.checkExisting()
        if existing:
            answer = profilerInstance.getOverviewLocal()
        else:
            answer = "No ingestion was done"
        return jsonify(answer), 200
    except Exception as e:
        return jsonify(str(e)), 500



