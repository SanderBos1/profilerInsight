from flask import Blueprint, jsonify, session
from ..userTables import userTable
from ..userConnections import dbConncetions
from ..userConnections import postgresqlConnection

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
        session['tableName'] = tableName
        userTableValues = userTable.query.filter(userTable.uniqueTableName==tableName).first()
        connection = dbConncetions.query.filter_by(connectionId=userTableValues.connectionId).first()   
        userDatabaseConnection = postgresqlConnection(connection.host, connection.port, connection.username, connection.password, connection.database)
        columns = userDatabaseConnection.query(f"SELECT table_name, column_name, data_type FROM information_schema.columns where table_name = '{userTableValues.table}' ORDER BY table_name, ordinal_position;")
        columnNames = []
        for tuple in columns:
            columnNames.append(tuple[1])

        answer = {
            "columnNames": columnNames,
            "columnCount": len(columnNames)

        }
        return jsonify(answer), 200
    except Exception as e:
        return jsonify(str(e)), 500
    


@profilerBP.route('/getOverview/<columName>', methods=['GET'])
def getOverview(columName):
    try:
        userTableValues = userTable.query.filter(userTable.uniqueTableName==session['tableName']).first()
        connection = dbConncetions.query.filter_by(connectionId=userTableValues.connectionId).first()   
        userDatabaseConnection = postgresqlConnection(connection.host, connection.port, connection.username, connection.password, connection.database)
        rowCount = userDatabaseConnection.query(f"select count(*) from {userTableValues.schema}.{ userTableValues.table}")

        distinctValues = userDatabaseConnection.query(f"SELECT COUNT(DISTINCT '{columName}')FROM {userTableValues.schema}.{userTableValues.table}")
        nanValues = userDatabaseConnection.query(f"SELECT COUNT(*) FROM {userTableValues.schema}.{userTableValues.table} WHERE '{columName}' IS NULL")
        columnType = userDatabaseConnection.query(f"SELECT data_type FROM information_schema.columns where table_name = '{userTableValues.table}' AND column_name = '{columName}'")
        print(columnType[0][0])
        answer = {
            "rowCount": rowCount[0][0],
            "distinctValues": distinctValues[0][0], 
            "nanValues": nanValues[0][0],
            "columnType": columnType[0][0]
        }
        return jsonify(answer), 200
    except Exception as e:
        return jsonify(str(e)), 500



