import os
import json
import logging
import io

from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from marshmallow import ValidationError

from src.schemas import CSVUploadSchema
from src.files import CsvHandler, XlsxHandler   
from src.loaders import FileLoader
from src.profiling import CheckType

file_profiler_bp = Blueprint(
    "file_profiler_bp",
    __name__,
)

@file_profiler_bp.route('/api/file_column_overview/<filename>/<column>', methods=['GET'])
def file_column_overview(filename:str, column:str):
    """
    Retrieve an overview of a specific column from a CSV file.

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
        # loads data & example
        profiler_generator = FileLoader(filename)
        example = profiler_generator.load_examples()

        # checks type of data
        data = profiler_generator.load(column)
        check_type = CheckType(data)
        profiler, data, dtype = check_type.check_type()

        # profiles data
        profiler_instance = profiler(data, column, dtype)
        profiler_overview = profiler_instance.profiler_output()

        return jsonify({
            "overview": profiler_overview,
            "example": example
        }), 200
    except FileNotFoundError as e:
        logging.error('FileNotFoundError: %s', e)
        return jsonify({"Error": "File not found."}), 404
    except json.JSONDecodeError as e:
        logging.error('JSONDecodeError: %s', e)
        return jsonify({"Error": "File could not be decoded"}), 400
    
@file_profiler_bp.route('/api/get_all_files', methods=['GET'])
def get_all_files():
    """
    Retrieve a list of all CSV files present in the configured directory.

    This endpoint scans the directory specified by the `csv_folder` configuration \
          and returns the filenames of CSV files without their extensions.

    Returns:
        Response: A JSON array containing the names of CSV files (without extensions) on success, \
            or an error message on failure, with HTTP status code 200 or 500.
    """
    try: 
        files = os.listdir(current_app.config['csv_folder'])
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
    Delete a specified  file and its associated properties file.

    This endpoint removes both the file and its JSON properties file from the configured directory.

    Args:
        filename (str): The name of the file to be deleted (without extension).

    Returns:
        Response: A JSON object with a success message on successful deletion, \
            or an error message on failure, with HTTP status code 200, 404, or 500.
    """
    try: 
        sec_filename =secure_filename(filename)
        filename = os.path.join(current_app.config['csv_folder'], f"{sec_filename}.csv")
        properties_filename = os.path.join(current_app.config['csv_folder'], f"{sec_filename}.json")
        os.remove(filename)
        os.remove(properties_filename)
        return jsonify(message="Success"), 200
    except FileNotFoundError as e:
        logging.error('FileNotFoundError: %s', e)
        return jsonify({"Error": "File not found."}), 404


@file_profiler_bp.route('/api/get_columns_file/<filename>', methods=['GET'])
def file_get_columns(filename:str):
    """
    Retrieve the list of column names from a specified CSV file.

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
        file_loader = FileLoader(filename)
        columns = file_loader.load_columns()
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
    Upload and processes a file with specified properties.

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
            flat_file_handler = CsvHandler(properties)
            df = flat_file_handler.clean(file)
            flat_file_handler.save_properties(filename)
            flat_file_handler.save(df, filename)
        else:
            xlsx_file = io.BytesIO(file.read())
            df = flat_file_handler = XlsxHandler(properties)
            flat_file_handler.save_properties(filename)
            flat_file_handler.clean(df, xlsx_file)
        return jsonify(message="Success"), 200
    except FileNotFoundError as e:
        logging.error('File Not Found: %s', e)
        return jsonify({"Error": "File not found."}), 404
    except IOError as e:
        logging.error('I/O Error: %s', e)
        return jsonify({"Error": "Error reading file."}), 500
    except ValueError as e:
        logging.error('Value Error: %s', e)
        return jsonify({"Error": "Invalid value provided."}), 400
