from flask import Blueprint, request, Response
import json 
from models import dbConncetions
from models.initializeDB import db


databaseBP = Blueprint(
    "databaseBP",
    __name__,
)

@databaseBP.route('/getConnections', methods=['GET'])
def getConnections():

    connectionList = dbConncetions.query.all()
    connections_dict_list = [connection.to_dict() for connection in connectionList]

    print(connections_dict_list)
    print(type(connections_dict_list))
    
    answer = json.dumps(connections_dict_list)

    return answer


@databaseBP.route('/addConnection', methods=['POST'])
def addConnection():
    body = request.get_json()
    print(body)
    try:
        Host = body['connectionHost']
        Port = body['connectionPort']
        Database = body['connectionDBName']
        UserName = body['connectionUser']
        Password = body['connectionPassword']
        DataBaseType = body['connectionType']
        new_connection = dbConncetions(Host=Host, Port=Port, DataBase=Database, UserName=UserName, Password=Password, DatabaseType=DataBaseType)
        db.session.add(new_connection)
        db.session.commit()
        return "Connection added successfully!", 200
    except Exception as e:
        return str(e), 500
