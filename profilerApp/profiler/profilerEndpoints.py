from flask import Blueprint, request, jsonify
from ..userTables import userTable
from ..userConnections import dbConncetions
from marshmallow import ValidationError
from ..userConnections import DatabaseConnection
from .jsonSchemas import overviewSchema 

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
@profilerBP.route('/getOverview', methods=['POST'])
def getOverview():
    try:
        overviewSchemaInstance = overviewSchema()
        data = overviewSchemaInstance.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 400
    try:
        userTableValues = userTable.query.filter(userTable.uniqueTableName==data['tableName']).first()
        connection = dbConncetions.query.filter_by(connectionId=userTableValues.connectionId).first()   
        print("connection", connection.host, connection.port, connection.username, connection.password, connection.database)
        userDatabaseConnection = DatabaseConnection(connection.host, connection.port, connection.username, connection.password, connection.database)
        rowCount = userDatabaseConnection.query(f"select count(*) from {userTableValues.schema}.{ userTableValues.table}")
        answer = {
            "rowCount": rowCount[0][0]
        }
        return jsonify(answer), 200
    except Exception as e:
        return str(e), 500