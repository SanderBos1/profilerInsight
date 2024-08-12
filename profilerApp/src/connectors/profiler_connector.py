"""
This module defines the `db_profiler_bp` Blueprint for handling database profiling 
and ingestion operations via various API endpoints. The endpoints facilitate interactions 
with database tables, including retrieving column information, ingesting data into a profiler, 
and obtaining column profiling details.

Key Components:
- `db_profiler_bp`: A Flask Blueprint used to group related routes for database profiling 
  and ingestion.
- `/api/get_columns/<table_id>`: An endpoint to retrieve column names for a specific table 
  identified by `table_id`.
- `/api/ingest/<table_id>/<column>`: An endpoint to ingest data from a specified column 
  of a table into the profiler.
- `/api/profile_column/<table_id>/<column>`: An endpoint to retrieve profiling information 
  for a specified column in a table.

Dependencies:
- `logging`: For logging errors and information.
- `flask`: For creating and managing Flask routes and responses.
- `numpy`: For handling and processing data arrays.
- `sqlalchemy.exc`: For handling database-related exceptions.
- `src.profiling`: For interacting with the `Profiler` class.
- `src.models`: For accessing database models like `DbConnections`, `ConnectedTables`, 
  and `IngestionOverview`.
- `src.config`: For retrieving database configuration.
- `src.database`: For handling database connections.

Usage:
    Import and register the `db_profiler_bp` Blueprint in a Flask application to enable 
    the defined API endpoints for database profiling and ingestion.

Example:
    from your_module import db_profiler_bp
    app.register_blueprint(db_profiler_bp)
"""

import logging

from flask import Blueprint, jsonify
import numpy as np
from sqlalchemy.exc import IntegrityError, OperationalError

from src.profiling import Profiler
from src.models import DbConnections, ConnectedTables, IngestionOverview
from src.config import get_database
from src.database import db_type_handler

db = get_database()


db_profiler_bp = Blueprint(
    "db_profiler_bp",
    __name__,
)

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
        table_info = ConnectedTables.query.filter_by(table_id=table_id).first()
        table_connection_id = table_info.connection_id
        table_tablename = table_info.tableName
        table_schema = table_info.schemaName
        connection = DbConnections.query.filter_by(connection_id=table_connection_id).first()
        password = connection.password
        connection_dict = connection.to_dict()
        new_db_connection = db_type_handler.get_database_connection(connection_dict['db_type'], \
                                                                    connection_dict, password)
        answer = new_db_connection.get_table_columns(table_schema, table_tablename)
        return jsonify(answer), 200
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Database operation failed"}), 500
    


@db_profiler_bp.route('/api/ingest/<table_id>/<column>', methods=['GET'])
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
        table_info = ConnectedTables.query.filter_by(table_id=table_id).first()
        table_connection_id = table_info.connection_id
        table_schema = table_info.schemaName
        table_tablename = table_info.tableName
        connection = DbConnections.query.filter_by(connection_id=table_connection_id).first()
        password = connection.password
        connection_dict = connection.to_dict()
        new_db_connection = db_type_handler.get_database_connection(connection_dict['db_type'],\
                                                                     connection_dict, password)
        answer = new_db_connection.get_column_data(table_schema, table_tablename, column)
        answer = np.array([row[0] for row in answer])

        profiler = Profiler(answer, table_tablename, column, table_id, table_connection_id)
        profiler.save_overview()
        return jsonify("Data Ingested"), 200
    except IntegrityError as e:
        logging.error('Integrity error: %s', e)
        db.session.rollback()
        return jsonify("Data already ingested"), 400
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Database operation failed"}), 500


@db_profiler_bp.route('/api/profile_column/<table_id>/<column>', methods=['GET'])
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
    try:
        if IngestionOverview.query.filter_by(table_id=table_id, column=column).first() is not None:
            overview = IngestionOverview.query.filter_by(table_id=table_id, column=column).first()
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
        return jsonify("No Dict Found"), 200
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Database operation failed"}), 500
