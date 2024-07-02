from flask import Blueprint, request, jsonify
import json 
from .models import dbConncetions
from profilerApp import db
from .jsonSchemas import ConnectionSchema, deleteConnectionSchema
from marshmallow import ValidationError

databaseBP = Blueprint(
    "databaseBP",
    __name__,
)

@databaseBP.route('/getConnections', methods=['GET'])
def getConnections():
    try:
        connectionList = dbConncetions.query.all()
        connections_dict_list = [connection.to_dict() for connection in connectionList]
        answer = json.dumps(connections_dict_list)
        return answer, 200
    except Exception as e:
        return str(e), 500

"""
    input: A JSOn object with the following structure:
        connectionId: str,
        host: str,
        port: str,
        username: str,
        password: str,
        database: str
    Goal: add the database connection to the database with the values provided in the JSON object
    output: a JSON object with the same structure as the input object
    status codes:
        200: the connection was added successfully
        400: the input JSON object is not valid
        500: an error occurred while adding the connection to the database

"""
@databaseBP.route('/addPostgresqlConnection', methods=['POST'])
def addConnection():
    try:
        connection_schema = ConnectionSchema()
        data = connection_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 400
    try:
        connectionId = data['connectionId']
        host = data['host']
        port = data['port']
        username = data['username']
        password = data['password']
        database = data['database']
        new_connection = dbConncetions(connectionId=connectionId, host=host, port=port, username=username, password=password, database=database)
        try:
            db.session.add(new_connection)
            db.session.commit()
        except Exception as e:
            return "Connection name has already been chosen", 500
        return data, 200
    except Exception as e:
        return jsonify(str(e)), 500


"""
    input: A JSOn object with the following structure:
        connectionId: str
    Goal: remove the database connectionfrom the database with the values provided in the JSON object
    output: a messages that indicates that the connection was removed succesfully
    status codes:
        200: the connection was added successfully
        400: the input JSON object is not valid
        500: an error occurred while adding the connection to the database

"""
@databaseBP.route('/deleteConnection', methods=['DELETE'])
def deleteConnection():
    try:
        connection_schema = deleteConnectionSchema()
        data = connection_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 400
    try:
        connectionId = data['connectionId']
        connection = dbConncetions.query.filter_by(connectionId=connectionId).first()
        db.session.delete(connection)
        db.session.commit()
        return "Connection deleted successfully!", 200
    except Exception as e:
        return jsonify(str(e)), 500


