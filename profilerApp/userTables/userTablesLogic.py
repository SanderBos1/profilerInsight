from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from .jsonSchemas import tableSchema, deleteTableSchema
from .models import userTable
from profilerApp import db
import json

usertableBP = Blueprint(
    "usertableBP",
    __name__,
)

@usertableBP.route('/getTables', methods=['GET'])
def getConnections():
    try:
        tabelList = userTable.query.all()
        dictTabelList = [connection.to_dict() for connection in tabelList]
        answer = json.dumps(dictTabelList)
        return answer, 200
    except Exception as e:
        return jsonify(str(e)), 500

"""
    input: A JSOn object with the following structure:
        connectionId: str,
        schema: str,
        table: str,
    Goal: Add the chosen table to the database
    output: a JSON object with the same structure as the input object
    status codes:
        200: the connection was added successfully
        400: the input JSON object is not valid
        500: an error occurred while adding the connection to the database

"""
@usertableBP.route('/addTable', methods=['POST'])
def addTable():
    try:
        connection_schema = tableSchema()
        data = connection_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 400
    try:
        uniqueTableName = data['uniqueTableName']
        connectionId = data['connectionId']
        schema = data['schema']
        table = data['table']
        new_connection = userTable(uniqueTableName=uniqueTableName, connectionId=connectionId, schema=schema, table=table)
        try:
            db.session.add(new_connection)
            db.session.commit()
        except Exception as e:
            return "the chosen table + schema have already been chosen", 500
        return data, 200
    except Exception as e:
        return jsonify(str(e)), 500
    

"""
    input: A JSOn object with the following structure:
        schema: str
        table: str
    Goal: remove the chosen table from the database with the values provided in the JSON object
    output: a messages that indicates that the connection was removed succesfully
    status codes:
        200: the connection was added successfully
        400: the input JSON object is not valid
        500: an error occurred while adding the connection to the database

"""
@usertableBP.route('/deleteTable', methods=['POST'])
def deleteTable():
    try:
        connection_schema = deleteTableSchema()
        data = connection_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify(e.messages), 400
    try:
        uniqueTableName = data['uniqueTableName']
        connection = userTable.query.filter_by(uniqueTableName=uniqueTableName).first()
        db.session.delete(connection)
        db.session.commit()
        return "Connection deleted successfully!", 200
    except Exception as e:
        return jsonify(str(e)), 500
