from flask import Blueprint, jsonify
from flasgger import swag_from
import numpy as np
from sqlalchemy.exc import IntegrityError

from src.profiling import Profiler
from ..models import dbConnections, connectedTables, ingestionOverview
from src import db
from..database import db_type_handler

db_profiler_bp = Blueprint(
    "db_profiler_bp",
    __name__,
)

@swag_from({
    'tags': ['Profiler'],
    'summary': 'Retrieve the columns of a table',
    'description': 'Gets the columns of the table identified by `table_id`. The method uses connection information stored in the database to connect to the appropriate database and fetch the column information.',
    'parameters': [
        {
            'name': 'table_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the table whose columns are to be retrieved.'
        }
    ],
    'responses': {
        '200': {
            'description': 'A JSON object containing the columns of the table.',
            'schema': {
                'type': 'object',
                'properties': {
                    'columns': {
                        'type': 'array',
                        'items': {
                            'type': 'string'
                        },
                        'description': 'List of column names in the table.'
                    }
                }
            }
        },
        '500': {
            'description': 'An error occurred while retrieving table columns.',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message describing what went wrong.'
                    }
                }
            }
        }
    }
})
@db_profiler_bp.route('/api/get_columns/<table_id>', methods=['GET'])
def get_columns(table_id:str):
    """
    Retrieve the columns of a table based on the table ID.

    This endpoint fetches the connection information for the specified table from the database,
    establishes a connection to the relevant database, and retrieves the column names of the table.

    Args:
    - table_id (string): The ID of the table whose columns are to be fetched.

    Returns:
    - JSON object with a list of column names if successful.
    - Error message if an exception occurs.
    """
    try:
        table_info = connectedTables.query.filter_by(table_id=table_id).first()
        table_connection_id = table_info.connection_id
        table_tablename = table_info.tableName
        table_schema = table_info.schemaName
        connection = dbConnections.query.filter_by(connection_id=table_connection_id).first()
        password = connection.password
        connection_dict = connection.to_dict()
        new_db_connection = db_type_handler.get_database_connection(connection_dict['db_type'], connection_dict, password)
        answer = new_db_connection.get_table_columns(table_schema, table_tablename)
        return jsonify(answer), 200
    except Exception as e:
        return jsonify(str(e)), 500
    


@db_profiler_bp.route('/api/ingest/<table_id>/<column>', methods=['GET'])
@swag_from({
    'tags': ['Profiler'],
    'summary': 'Ingest data from a specified column into the profiler',
    'description': 'Fetches data from a specified column of a table identified by `table_id` and ingests it into the profiler. The method uses connection information stored in the database to connect to the appropriate database and fetch the column data.',
    'parameters': [
        {
            'name': 'table_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the table from which data will be ingested.'
        },
        {
            'name': 'column',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Name of the column to ingest data from.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Data successfully ingested into the profiler.',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Data Ingested'
                    }
                }
            }
        },
        '400': {
            'description': 'Data already ingested.',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Data already ingested'
                    }
                }
            }
        },
        '500': {
            'description': 'An error occurred while processing the request.',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Error message describing what went wrong.'
                    }
                }
            }
        }
    }
})
def db_profiler_ingestion(table_id:str, column:str):
    """
    Ingests data from a specified column of a table into the profiler.

    Fetches data from the specified column of the table identified by `table_id`.
    The data is then processed and ingested into the profiler system.

    Args:
    - table_id (string): The ID of the table from which the data is to be fetched.
    - column (string): The name of the column to fetch data from.

    Returns:
    - JSON object with a success message if data is ingested successfully.
    - JSON object with an error message if the data is already ingested or if an exception occurs.
    """
    try:
        table_info = connectedTables.query.filter_by(table_id=table_id).first()
        table_connection_id = table_info.connection_id
        table_schema = table_info.schemaName
        table_tablename = table_info.tableName
        connection = dbConnections.query.filter_by(connection_id=table_connection_id).first()
        password = connection.password
        connection_dict = connection.to_dict()
        new_db_connection = db_type_handler.get_database_connection(connection_dict['db_type'], connection_dict, password)
        answer = new_db_connection.get_column_data(table_schema, table_tablename, column)
        answer = np.array([row[0] for row in answer])
    except Exception as e:
        return jsonify(str(e)), 500
    try:
        profiler = Profiler(answer, table_tablename, column, table_id, table_connection_id)
        profiler.save_overview()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify("Data already ingested"), 400
    return jsonify("Data Ingested"), 200


@db_profiler_bp.route('/api/profile_column/<table_id>/<column>', methods=['GET'])
@swag_from({
    'tags': ['Profiler'],
    'summary': 'Get the ingestion overview for a specified column',
    'description': 'Retrieves the ingestion overview information for the specified column of a table identified by `table_id`. The overview includes metrics such as column length, number of NaNs, number of unique values, and column type.',
    'parameters': [
        {
            'name': 'table_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the table for which the column overview is requested.'
        },
        {
            'name': 'column',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Name of the column for which the overview is requested.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Overview information of the column.',
            'schema': {
                'type': 'object',
                'properties': {
                    'column_length': {
                        'type': 'integer',
                        'description': 'The length of the column.'
                    },
                    'number_nans': {
                        'type': 'integer',
                        'description': 'Number of NaN values in the column.'
                    },
                    'number_unique': {
                        'type': 'integer',
                        'description': 'Number of unique values in the column.'
                    },
                    'column_type': {
                        'type': 'string',
                        'description': 'Data type of the column.'
                    }
                }
            }
        },
        '404': {
            'description': 'No overview found for the specified table ID and column.',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'No Dict Found'
                    }
                }
            }
        }
    }
})
def db_profiler(table_id:str,  column:str):
    """
    Retrieves the ingestion overview for a specified column in a table.

    Fetches metrics such as column length, number of NaN values, number of unique values,
    and column type for the specified column and table.

    Args:
    - table_id (string): The ID of the table for which the overview is requested.
    - column (string): The name of the column for which the overview is requested.

    Returns:
    - JSON object containing column overview information if found.
    - JSON object with a message indicating no overview was found.
    """
    if ingestionOverview.query.filter_by(table_id=table_id, column=column).first() is not None:
        overview = ingestionOverview.query.filter_by(table_id=table_id, column=column).first()
        overview_dict = {
            "column_length": overview.column_length,
            "number_nans": overview.number_nans,
            "number_unique": overview.number_unique,
            "number_distinct": overview.number_distinct,
            "column_type": overview.column_type,
            "data_preview": overview.data_preview,
            "mean_value": overview.mean_value,
            "median_value": overview.median_value,
            "min_value": overview.min_value,
            "max_value": overview.max_value,
            "patterns": overview.patterns,
            "histogram": overview.histogram,
            "boxplot": overview.boxplot
        }
        return jsonify(overview_dict), 200
    else:
        return jsonify("No Dict Found"), 200



