"""
This module provides routes for managing file operations related to CSV and XLSX files. 

Key Routes:
- `/api/file_column_overview/<filename>/<column>`: Retrieves an overview of a specific column from
    a CSV file, including profiling information.
- `/api/get_all_files`: Lists all CSV files present in the configured directory.
- `/api/delete_file/<filename>`: Deletes the specified file 
    and its associated properties file from the configured directory.
- `/api/get_columns_file/<filename>`: Retrieves the list of column names from a specified CSV file.
- `/api/upload_file`: Handles the upload and processing of CSV or XLSX files, 
    including validation of file properties.

Dependencies:
- `flask`: Used for creating and managing Flask routes and handling HTTP requests and responses.
- `werkzeug`: Provides utilities for file handling, such as `secure_filename`.
- `marshmallow`: Used for schema validation and deserialization.
- `src.schemas`: Contains the `CSVUploadSchema` for validating upload request data.
- `src.files`: Includes `FileHandler` for handling file operations.
- `src.profiling`: Provides `FileProfiler` for profiling file contents.

Configuration:
- The `csvFolder` configuration should specify the directory where CSV files are stored and managed.

Error Handling:
- The module handles various exceptions, including `FileNotFoundError`, `json.JSONDecodeError`, 
`IOError`, and `ValueError`, returning appropriate error messages and HTTP status codes.

Usage:
    Import and register the `file_profiler_bp` Blueprint in a Flask application 
    to enable the defined routes for file operations and profiling.

Example:
    from your_module import file_profiler_bp
    app.register_blueprint(file_profiler_bp)
"""

import os
import json
import logging
import io

from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from marshmallow import ValidationError

from src.schemas import CSVUploadSchema
from src.files import FileHandler
from src.profiling  import FileProfiler

file_profiler_bp = Blueprint(
    "file_profiler_bp",
    __name__,
)

@file_profiler_bp.route('/api/file_column_overview/<filename>/<column>', methods=['GET'])
def file_column_overview(filename:str, column:str):
    """
    Retrieves an overview of a specific column from a CSV file.

    This endpoint provides profiling information for the specified column, 
    including statistics and visualizations. 

    Args:
        filename (str): The name of the CSV file (without extension).
        column (str): The name of the column to profile.

    Returns:
        Response: A JSON object containing column profiling information on success, 
        or an error message on failure, with HTTP status code 200, 400, 404, or 500.
    """
    filename = secure_filename(filename)
    try:
        profiler_generator = FileProfiler(filename)
        columns = profiler_generator.profile_file(column)
        return jsonify(columns), 200
    except FileNotFoundError as e:
        logging.error('FileNotFoundError: %s', e)
        return jsonify({"Error": "File not found."}), 404
    except json.JSONDecodeError as e:
        logging.error('JSONDecodeError: %s', e)
        return jsonify({"Error": "File could not be decoded"}), 400
    
@file_profiler_bp.route('/api/get_all_files', methods=['GET'])
def get_all_files():
    """
    Retrieves a list of all CSV files present in the configured directory.

    This endpoint scans the directory specified by the `csvFolder` configuration \
          and returns the filenames of CSV files without their extensions.

    Returns:
        Response: A JSON array containing the names of CSV files (without extensions) on success, \
            or an error message on failure, with HTTP status code 200 or 500.
    """
    try: 
        files = os.listdir(current_app.config['csvFolder'])
        filenames = []
        for file in files:
            filename = file.split(".")
            if filename[1] == "csv":
                filenames.append(filename[0])
        return jsonify(filenames), 200
    except FileNotFoundError as e:
        logging.error('FileNotFoundError: %s', e)
        return jsonify({"Error": "File not found."}), 404
    
@file_profiler_bp.route('/api/delete_file/<filename>', methods=['DELETE'])
def delete_file(filename):
    """
    Deletes a specified  file and its associated properties file.

    This endpoint removes both the file and its JSON properties file from the configured directory.

    Args:
        filename (str): The name of the file to be deleted (without extension).

    Returns:
        Response: A JSON object with a success message on successful deletion, \
            or an error message on failure, with HTTP status code 200, 404, or 500.
    """
    try: 
        sec_filename =secure_filename(filename)
        filename = os.path.join(current_app.config['csvFolder'], f"{sec_filename}.csv")
        properties_filename = os.path.join(current_app.config['csvFolder'], f"{sec_filename}.json")
        os.remove(filename)
        os.remove(properties_filename)
        return jsonify(message="Success"), 200
    except FileNotFoundError as e:
        logging.error('FileNotFoundError: %s', e)
        return jsonify({"Error": "File not found."}), 404


@file_profiler_bp.route('/api/get_columns_file/<filename>', methods=['GET'])
def file_get_columns(filename:str):
    """
    Retrieves the list of column names from a specified CSV file.

    This endpoint loads the specified CSV file and its associated properties file, \
        then returns a list of column names found in the CSV file.

    Args:
        filename (str): The name of the CSV file (without extension) to retrieve column names from.

    Returns:
        Response: A JSON array containing the column names on success, \
            or an error message on failure, with HTTP status code 200, 400, 404, or 500.
    """
    filename = secure_filename(filename)
    try:
        profiler_generator = FileProfiler(filename)
        columns = profiler_generator.get_columns()
        return jsonify(columns), 200
    except FileNotFoundError as e:
        logging.error('FileNotFoundError: %s', e)
        return jsonify({"Error": "File not found."}), 404
    except json.JSONDecodeError as e:
        logging.error('JSONDecodeError: %s', e)
        return jsonify({"Error": "File could not be decoded"}), 400



@file_profiler_bp.route('/api/upload_file', methods=['POST'])
def upload_file():
    """
    Uploads and processes a file with specified properties.

    This endpoint handles the upload of a CSV or XLSX file, \
        validates the form data including delimiter, header row, and quote character, \
            and processes the file accordingly. \
                The processing depends on the file type and specified properties.

    Form Data Parameters:
        - flatDataSet (file): The CSV or XLSX file to be uploaded and processed.
        - csvSeperator (string, default: ','): The delimiter used in the CSV file.
        - header_row (integer, default: 0): The row number (0-based index) \
            containing header information.
        - quoteChar (string, default: '"'): The character used to quote fields in the CSV file.

    Returns:
        Response: A JSON object with a success message on successful processing, \
            or an error message on failure, with HTTP status code 200, 400, or 500.
    """
    try:
        csv_upload_form = CSVUploadSchema()
        data = csv_upload_form.load(request.form)
    except ValidationError as e:
        logging.error('Validation Error: %s', e)
        return jsonify({"Error": "Incorrect Data"}), 400
    try:

        file = request.files['flatDataSet']
        filename, ext = os.path.splitext(file.filename)
        filename = secure_filename(filename)

        delimiter = data.get('csvSeperator', ',')
        header_row = data.get('headerRow', 0) 
        quotechar = data.get('quoteChar', '"') 

        properties = {
            'delimiter': delimiter,
            'header_row': header_row,
            'quotechar': quotechar
        }

        if ext == '.csv':
            flat_file_handler = FileHandler(filename, properties)
            flat_file_handler.upload_csv(file)
        else:
            xlsx_file = io.BytesIO(file.read())
            flat_file_handler = FileHandler(filename, properties)
            flat_file_handler.upload_xlsx(xlsx_file)
        return jsonify(message="Success"), 200
    except FileNotFoundError as e:
        logging.error('File Not Found: %s', e)
        return jsonify({"error": "File not found."}), 404
    except IOError as e:
        logging.error('I/O Error: %s', e)
        return jsonify({"error": "Error reading file."}), 500
    except ValueError as e:
        logging.error('Value Error: %s', e)
        return jsonify({"error": "Invalid value provided."}), 400
