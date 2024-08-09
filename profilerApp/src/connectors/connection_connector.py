from flask import Blueprint, request, jsonify
from src.models import dbConnections, connectedTables, ingestionOverview
from src.database import db_type_handler   
from src.schemas import ConnectionSchema
from marshmallow import ValidationError
from src import db
from flasgger import swag_from
from sqlalchemy.exc import OperationalError

connections_bp = Blueprint(
    "connections_bp",
    __name__
)


@connections_bp.route('/api/get_connected_tables', methods=['GET'])
@swag_from({
    'tags': ['Database'],
    'description': 'Fetches all connected tables and returns them as a JSON array.',
    'responses': {
        '200': {
            'description': 'A list of connected tables',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'table_id': {
                            'type': 'integer',
                            'description': 'Unique identifier for the table entry'
                        },
                        'connection_id': {
                            'type': 'string',
                            'description': 'Identifier of the associated database connection'
                        },
                        'schemaName': {
                            'type': 'string',
                            'description': 'Schema name in the database'
                        },
                        'tableName': {
                            'type': 'string',
                            'description': 'Name of the table'
                        }
                    }
                }
            }
        },
        '500':{

            'description': 'Database error occurred'

        },
        '500': {
            'description': 'Internal Server Error'
        }
    }
})
def get_connected_tables():
    try:
        connected_tables = connectedTables.query.all()
        connected_table_list = [connected_table.to_dict() for connected_table in connected_tables]
        return jsonify({'Answer': connected_table_list}), 200
    except OperationalError as e:
        return jsonify({"Error": "Database error occurred", "details": str(e)}), 500
    except Exception as e:
        return jsonify(str(e)), 500
    


@connections_bp.route('/api/ingest_connected_tables', methods=['GET'])
@swag_from({
    'tags': ['Database'],
    'description': 'Ingests tables from all database connections into the connectedTables model. Each connection\'s tables are retrieved and stored in the database.',
    'responses': {
        '200': {
            'description': 'Successfully loaded tables from all connections.',
            'schema': {
                'type': 'string',
                'example': 'Loaded'
            }
        },
        '500': {
            'description': 'Internal Server Error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message describing what went wrong'
                    }
                }
            }
        }
    }
})
def ingest_connected_table():
    """
    Ingests tables from all database connections into the connectedTables model.

    This endpoint retrieves all database connections, uses each connection to get tables from a PostgreSQL database,
    and inserts the tables into the `connectedTables` model.

    Returns:
        Response: A JSON response indicating success or failure, with HTTP status code 200 or 500.
    """
    try:
        connection_list = dbConnections.query.all()
        for connection in connection_list:
            password = connection.password
            connection_dict = connection.to_dict()
            new_db_connection = db_type_handler.get_database_connection(connection_dict['db_type'], connection_dict, password)
            answer = new_db_connection.get_all_tables()
            for item in answer:
                new_connection = connectedTables(connection_id = connection.connection_id, schemaName = item[0], tableName = item[1])
                db.session.add(new_connection)
                db.session.commit()
        return jsonify({"Message": "connection_loaded"}), 200
    except OperationalError as e:
        return jsonify({"Error": "Something went wrong in the database"}), 500
    except Exception as e:
        return jsonify(str(e)), 500

    
@connections_bp.route('/api/get_connections', methods=['GET'])
@swag_from({
    'tags': ['Database'],
    'description': 'Retrieves all database connections and returns them as a JSON array.',
    'responses': {
        '200': {
            'description': 'A list of database connections',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'connection_id': {
                            'type': 'string',
                            'description': 'Unique identifier for the connection'
                        },
                        'host': {
                            'type': 'string',
                            'description': 'Host of the database connection'
                        },
                        'port': {
                            'type': 'string',
                            'description': 'Port of the database connection'
                        },
                        'username': {
                            'type': 'string',
                            'description': 'Username for the database connection'
                        },
                        'database': {
                            'type': 'string',
                            'description': 'Database name for the connection'
                        }
                    }
                }
            }
        },
        '500': {
            'description': 'Internal Server Error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message describing what went wrong'
                    }
                }
            }
        }
    }
})
def get_connections():
    """
    Handles the GET request to retrieve all database connections.

    Queries the database for all entries in the `dbConnections` model, converts each entry to a dictionary,
    and returns the result as a JSON response.

    Returns:
        Response: A JSON response containing a list of dictionaries, each representing a database connection,
        with HTTP status code 200 or 500.
    """
    try:
        connection_list = dbConnections.query.all()
        connections_dict_list = [connection.to_dict() for connection in connection_list]
        return jsonify({'Answer': connections_dict_list}), 200
    except OperationalError as e:
        return jsonify({"Error": "Something went wrong in the database"}), 500
    except Exception as e:
        return jsonify({"Error": "Something went wrong", "details": str(e)}), 500


@connections_bp.route('/api/add_postgres_connection', methods=['POST'])
@swag_from({
    'tags': ['Database'],
    'description': 'Adds a new PostgreSQL connection to the database. Requires connection details to be sent in the request body.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'description': 'Details of the PostgreSQL connection to add.',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'connection_id': {
                        'type': 'string',
                        'description': 'Unique identifier for the connection'
                    },
                    'host': {
                        'type': 'string',
                        'description': 'Host of the PostgreSQL server'
                    },
                    'port': {
                        'type': 'string',
                        'description': 'Port of the PostgreSQL server'
                    },
                    'username': {
                        'type': 'string',
                        'description': 'Username for the PostgreSQL connection'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Password for the PostgreSQL connection'
                    },
                    'database': {
                        'type': 'string',
                        'description': 'Database name to connect to'
                    }
                },
                'required': ['connection_id', 'host', 'port', 'username', 'password', 'database']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Successfully added the PostgreSQL connection',
            'schema': {
                'type': 'object',
                'properties': {
                    'connection_id': {
                        'type': 'string',
                        'description': 'Unique identifier for the connection'
                    },
                    'host': {
                        'type': 'string',
                        'description': 'Host of the PostgreSQL server'
                    },
                    'port': {
                        'type': 'string',
                        'description': 'Port of the PostgreSQL server'
                    },
                    'username': {
                        'type': 'string',
                        'description': 'Username for the PostgreSQL connection'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Password for the PostgreSQL connection'
                    },
                    'database': {
                        'type': 'string',
                        'description': 'Database name to connect to'
                    }
                }
            }
        },
        '400': {
            'description': 'Validation error in the request data',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'object',
                        'description': 'Details of validation errors'
                    }
                }
            }
        },
        '500': {
            'description': 'Internal Server Error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message describing what went wrong'
                    }
                }
            }
        }
    }
})
def add_postgres_connection():
    """
    Handles the POST request to add a new PostgreSQL connection.

    Expects connection details to be provided in the request body. Validates the input data, creates a new `dbConnections`
    entry, and commits it to the database.

    Returns:
        Response: A JSON response with the connection details on success, or an error message on failure, with HTTP status code 200, 400, or 500.
    """
    try:
        connection_schema = ConnectionSchema()
        data = connection_schema.load(request.get_json())
    except ValidationError as e:
        return jsonify({"Error": "Incorrect Data"}), 400
    try:
        connection_id = data['connection_id']
        host = data['host']
        port = data['port']
        username = data['username']
        password = data['password']
        database = data['database']
        db_type = data['db_type']
        new_connection = dbConnections(connection_id=connection_id, host=host, port=port, username=username, password=password, database=database, db_type=db_type)
        try:
            db.session.add(new_connection)
            db.session.commit()
            return jsonify({"Message":"Connection Added Succesfully!"}), 200
        except Exception as e:
            return jsonify({"Error": "Connection_id already exists"}), 500
    except OperationalError as e:
        return jsonify({"Error": "Database operation failed", "details": str(e)}), 500
    except Exception as e:
        return jsonify(str(e)), 500



@connections_bp.route('/api/delete_connection/<connection_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Database'],
    'description': 'Deletes a PostgreSQL connection along with associated connected tables and ingestion records.',
    'parameters': [
        {
            'name': 'connection_id',
            'in': 'path',
            'description': 'The unique identifier of the connection to be deleted.',
            'required': True,
            'schema': {
                'type': 'string',
                'example': 'conn_123'
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Successfully deleted the connection along with related records.',
            'schema': {
                'type': 'string',
                'example': 'Connection deleted successfully!'
            }
        },
        '404': {
            'description': 'Connection not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message indicating the connection was not found'
                    }
                }
            }
        },
        '500': {
            'description': 'Internal Server Error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message describing what went wrong'
                    }
                }
            }
        }
    }
})
def delete_connection(connection_id:str):
    """
    Handles the DELETE request to remove a PostgreSQL connection and its related records.

    This endpoint deletes the specified connection, along with any tables and ingestion records associated with it.

    Args:
        connection_id (str): The unique identifier of the connection to be deleted.

    Returns:
        Response: A JSON response indicating the success or failure of the operation, with HTTP status code 200, 404, or 500.
    """
    try:
        connection = dbConnections.query.filter_by(connection_id=connection_id).first()
        if connection is None:
            return jsonify({'Error': 'Connection not found'}), 404
        connected_tables = connectedTables.query.filter_by(connection_id=connection_id)
        ingestions = ingestionOverview.query.filter_by(connection_id=connection_id)
        for ingestion in ingestions:
            db.session.delete(ingestion)
        for table in connected_tables:
            db.session.delete(table)
        db.session.delete(connection)
        db.session.commit()
        return jsonify({'Message':"Connection deleted successfully!"}), 200
    except Exception as e:
        return jsonify({'Error': str(e)}), 500


