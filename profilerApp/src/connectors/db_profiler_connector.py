import logging

from flask import Blueprint, jsonify
from sqlalchemy.exc import IntegrityError, OperationalError

from src.models import IngestionOverview
from src.config import SingletonDB
from src.loaders import DbLoader
from src.profiling import CheckType

DB = SingletonDB.get_instance()


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
        new_loader = DbLoader()
        columns = new_loader.load_columns(table_id)
        return jsonify(columns), 200
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Database operation failed"}), 500
    


@db_profiler_bp.route('/api/ingest/<table_id>/<column>', methods=['GET'])
def db_profiler_ingestion(table_id:str, column:str):
    """
    Ingest data from a specified column of a table into the backend database.

    Fetches data from the specified column of the table identified by `table_id`.
    The data is then processed and ingested into the profiler system.

    Args:
        - table_id (string): The ID of the table from which the data is to be fetched.
        - column (string): The name of the column to fetch data from.

    Returns:
        - JSON object with a success message if data is ingested successfully.
        - JSON object with an error message if the data is already ingested 
            or if an exception occurs.
    """
    try:
        # loads data & example
        profiler_generator = DbLoader()

        # checks type of data
        data, table_name, connection_id = profiler_generator.load(column, table_id)
        check_type = CheckType(data)
        profiler, data, dtype = check_type.check_type()

        # profiles data
        profiler_instance = profiler(data, column, dtype)
        profiler_overview = profiler_instance.profiler_output()

        # ingest into database
        ingestion_overview = IngestionOverview(
            table=table_name,
            column=profiler_overview['column'],
            table_id = table_id,
            connection_id = connection_id,
            column_type=profiler_overview['column_type'],
            column_length=profiler_overview['column_length'],
            median_value=profiler_overview['mean'],
            mean_value=profiler_overview['median'],
            min_value=profiler_overview['min'],
            max_value=profiler_overview['max'],
            number_unique=profiler_overview['unique_values'],
            number_distinct=profiler_overview['distinct_values'],
            number_nans=profiler_overview['nan_percantage'],
            patterns=profiler_overview.get('patterns', None),
            boxplot=profiler_overview.get('boxplot', None),
            histogram=profiler_overview.get('histogram', None),
        )

        DB.session.merge(ingestion_overview)
        DB.session.commit()

        return jsonify({
            "Message": "Data Ingested"}), 200
    except IntegrityError as e:
        logging.error('Integrity error: %s', e)
        DB.session.rollback()
        return jsonify({"Error":"Data already ingested"}), 400
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Database operation failed"}), 500


@db_profiler_bp.route('/api/profile_column/<table_id>/<column>', methods=['GET'])
def db_profiler(table_id:str,  column:str):
    """
    Retrieve the ingestion overview for a specified column in a table.

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
        profiler_generator = DbLoader()
        example = profiler_generator.load_examples(table_id)

        if IngestionOverview.query.filter_by(table_id=table_id, column=column).first() is not None:
            overview = IngestionOverview.query.filter_by(table_id=table_id, column=column).first()
            overview_dict = {
                "column_length": overview.column_length,
                "nan_percantage": overview.number_nans,
                "unique_values": overview.number_unique,
                "distinct_values": overview.number_distinct,
                "column_type": overview.column_type,
                "mean": overview.mean_value,
                "median": overview.median_value,
                "min": overview.min_value,
                "max": overview.max_value,
                "pattern": overview.patterns,
                "histogram": overview.histogram,
                "boxplot": overview.boxplot
            }
            return jsonify({
                "overview": overview_dict,
                "example": example
            }), 200        
        return jsonify("No Dict Found"), 200
    except OperationalError as e:
        logging.error('Database error occurred: %s', e)
        return jsonify({"Error": "Database operation failed"}), 500
