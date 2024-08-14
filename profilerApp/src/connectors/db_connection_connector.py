import logging

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from sqlalchemy.exc import OperationalError, IntegrityError 
from src.config import SingletonDB
from src.models import DbConnections, ConnectedTables, IngestionOverview
from src.database import get_database_connection   
from src.schemas import ConnectionSchema

DB = SingletonDB.get_instance()

connections_bp = Blueprint(
    "connections_bp",
    __name__
)


@connections_bp.route('/api/get_connected_tables', methods=['GET'])
def get_connected_tables():
    """
    Handle the GET request for retrieving a list of connected tables.

    This endpoint queries the database for all connected tables and returns
    their details in a JSON format. Each connected table is represented as
    a dictionary. If an error occurs during the database operation or any
    other exception, an appropriate error message is logged and returned.

    Returns:
        Response: A JSON response containing either the list of connected
                  tables or an error message, along with an HTTP status code.        
    Raises:
        OperationalError
    """
    try:
        connected_tables = ConnectedTables.query.all()
        connected_table_list = [connected_table.to_dict() for connected_table in connected_tables]
        return jsonify({'Answer': connected_table_list}), 200
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Database error occurred"}), 500


@connections_bp.route('/api/ingest_connected_tables', methods=['GET'])
def ingest_connected_table():
    """
    Ingests tables from all database connections into the ConnectedTables model.

    This endpoint retrieves all database connections, 
    uses each connection to get tables from a PostgreSQL database,
    and inserts the tables into the `ConnectedTables` model.

    Returns:
        Response: A JSON response indicating success or failure, with HTTP status code 200 or 500.

    Raises:
        OperationalError
    """
    try:
        connection_list = DbConnections.query.all()
        for connection in connection_list:
            password = connection.password
            connection_dict = connection.to_dict()
            new_db_connection = get_database_connection(connection_dict['db_type'],\
                                                                         connection_dict, password)
            answer = new_db_connection.get_all_tables()
            for item in answer:
                new_connection = ConnectedTables(connection_id = connection.connection_id,\
                                                  schemaName = item[0], tableName = item[1])
                DB.session.add(new_connection)
                DB.session.commit()
        return jsonify({"Message": "connection_loaded"}), 200
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Something went wrong in the database"}), 500
    
@connections_bp.route('/api/get_connections', methods=['GET'])
def get_connections():
    """
    Handle the GET request to retrieve all database connections.

    Queries the database for all entries in the `DbConnections` model, 
    converts each entry to a dictionary,
    and returns the result as a JSON response.

    Returns:
        Response: A JSON response containing a list of dictionaries,
        each representing a database connection,
        with HTTP status code 200 or 500.

    Raises:
        OperationalError
    """
    try:
        connection_list = DbConnections.query.all()
        connections_dict_list = [connection.to_dict() for connection in connection_list]
        return jsonify({'Answer': connections_dict_list}), 200
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify('Database error occurred: %s', e), 500

@connections_bp.route('/api/add_postgres_connection', methods=['POST'])
def add_postgres_connection():
    """
    Handle the POST request to add a new PostgreSQL connection.

    Expects connection details to be provided in the request body. Validates the input data, 
    creates a new `DbConnections`
    entry, and commits it to the database.

    Returns:
        Response: A JSON response with the connection details on success, 
        or an error message on failure, with HTTP status code 200, 403, or 500.

    Raises:
        OperationalError
    """
    try:
        connection_schema = ConnectionSchema()
        data = connection_schema.load(request.get_json())
    except ValidationError as e:
        logging.error('Validation Error: %s', e)
        return jsonify({"Error": "Incorrect Data"}), 400
    try:
        connection_id = data['connection_id']
        host = data['host']
        port = data['port']
        username = data['username']
        password = data['password']
        database = data['database']
        db_type = data['db_type']
        new_connection = DbConnections(connection_id=connection_id, host=host, \
                                       port=port, username=username, password=password, \
                                        database=database, db_type=db_type)
        try:
            DB.session.add(new_connection)
            DB.session.commit()
            return jsonify({"Message":"Connection Added Succesfully!"}), 200
        except IntegrityError as e:
            DB.session.rollback()
            logging.error('Integrity error: %s', e)
            return jsonify({"Error": "Connection_id already exists"}), 403
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Database operation failed"}), 500

@connections_bp.route('/api/delete_connection/<connection_id>', methods=['DELETE'])
def delete_connection(connection_id:str):
    """
    Handle the DELETE request to remove a PostgreSQL connection and its related records.

    This endpoint deletes the specified connection, 
    along with any tables and ingestion records associated with it.

    Args:
        connection_id (str): The unique identifier of the connection to be deleted.

    Returns:
        Response: A JSON response indicating the success or failure of the operation, 
        with HTTP status code 200, 404, or 500.

    Raises:
        OperationalError
        IntegrityError
    """
    try:
        connection = DbConnections.query.filter_by(connection_id=connection_id).first()
        if connection is None:
            return jsonify({'Error': 'Connection not found'}), 404
        connected_tables = ConnectedTables.query.filter_by(connection_id=connection_id)
        ingestions = IngestionOverview.query.filter_by(connection_id=connection_id)
        for ingestion in ingestions:
            DB.session.delete(ingestion)
        for table in connected_tables:
            DB.session.delete(table)
        DB.session.delete(connection)
        DB.session.commit()
        return jsonify({'Message':"Connection deleted successfully!"}), 200
    except IntegrityError as e:
        DB.session.rollback()
        logging.error('Integrity error: %s', e)
        return jsonify({"Error": "Connection_id already exists"}), 403
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Database operation failed"}), 500
