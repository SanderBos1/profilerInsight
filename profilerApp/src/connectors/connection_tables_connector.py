import logging


from flask import Blueprint, jsonify
from sqlalchemy.exc import OperationalError

from src.models import ConnectedTables
from src.config import SingletonDB

connection_tables_bp = Blueprint(
    "connection_tables_bp",
    __name__
)


DB = SingletonDB.get_instance()


@connection_tables_bp.route('/api/get_connected_tables', methods=['GET'])
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
    

@connection_tables_bp.route('/api/load_tables/<connection_id>', methods=['GET'])
def load_tables(connection_id:str):
    """
    Handle the GET request to load tables from a database connection.

    This endpoint retrieves the tables from the specified database connection
    and inserts them into the `ConnectedTables` model. If an error occurs during
    the database operation or any other exception, an appropriate error message
    is logged and returned.

    Args:
        connection_id (str): The unique identifier of the database connection.

    Returns:
        Response: A JSON response indicating success or failure, along with an
                  HTTP status code.
    Raises:
        OperationalError
    """
    try:
        tables = ConnectedTables.query.filter_by(connection_id=connection_id).all()
        tables = [table.to_dict() for table in tables]     
        return jsonify({"Answer": tables}), 200
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Something went wrong in the database"}), 500
    
@connection_tables_bp.route('/api/get_table_info/<table_id>', methods=['GET'])
def get_connection_info(table_id:str):
    """
    Handle the GET request to retrieve the connection ID of a table.

    This endpoint retrieves the connection ID of the specified table
    from the `ConnectedTables` model and returns it as a JSON response.
    If the table is not found, an appropriate error message is returned.

    Args:
        table_id (str): The unique identifier of the table.

    Returns:
        Response: A JSON response containing the connection ID of the table,
                  or an error message if the table is not found, along with an
                  HTTP status code.
    Raises: 
        OperationalError
    
    """
    try:
        table = ConnectedTables.query.filter_by(table_id=table_id).first()
        if table is None:
            return jsonify({'Error': 'Table not found'}), 404
        return jsonify({'Answer': table.to_dict()}), 200
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Something went wrong in the database"}), 500