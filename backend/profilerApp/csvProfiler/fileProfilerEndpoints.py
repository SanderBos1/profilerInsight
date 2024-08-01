from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
import os
import json
from .jsonSchemas import csvUploadSchema
from .fileProfiler import CSVProfiler
import io

csvProfilerBP = Blueprint(
    "csvProfilerBP",
    __name__,
)

@csvProfilerBP.route('/getColumnOverview/<filename>/<column>', methods=['GET'])
def getColumnOverview(filename:str, column:str):
    """
    Retrieve the overview of a specific column in a CSV file.

    This endpoint loads a CSV file and its properties, processes the specified column,
    and returns the profiling information.

    Parameters:
    filename (str): The name of the CSV file (without extension).
    column (str): The name of the column to profile.

    Returns:
        Tuple[dict, int]: A JSON response containing the column profiling information and the HTTP status code.

    Status Codes:
        200: Successful retrieval of column profiling information.
        404: File not found (either CSV or properties file).
        400: Error decoding JSON properties file.
        500: General server error (any other exceptions).


    """
    filename = secure_filename(filename)
    try:
        propertiesFileName = os.path.join(current_app.config['csvFolder'], f"{filename}.json")
        with open(propertiesFileName, 'rb') as properties:
            properties = json.load(properties)

        newCSVProfiler = CSVProfiler(filename, properties)
        newCSVProfiler.loadCSV()
        columns = newCSVProfiler.csvProfiler(column)
        return jsonify(columns), 200
    
    except FileNotFoundError:
        error_message = f"File {filename}.json not found."
        current_app.logger.error(error_message)
        return jsonify({"error": error_message}), 404
    
    except json.JSONDecodeError:
        error_message = f"Error decoding JSON in file {filename}.json."
        current_app.logger.error(error_message)
        return jsonify({"error": error_message}), 400
    
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

@csvProfilerBP.route('/getCSVFiles', methods=['GET'])
def getCSVFiles():
    """
    Retrieve a list of all CSV files in the configured directory.

    This endpoint scans the configured directory for CSV files and returns their filenames without extensions.

    Returns:
    Tuple[dict, int]: A JSON response containing a list of CSV filenames and the HTTP status code.

    Status Codes:
    200: Successful retrieval of CSV filenames.
    500: General server error (any other exceptions).

    """
    try: 
        files = os.listdir(current_app.config['csvFolder'])
        filenames = []
        for file in files:
            filename = file.split(".")
            if filename[1] == "csv":
                filenames.append(filename[0])
        return jsonify(filenames), 200
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
    
@csvProfilerBP.route('/deleteCSVFile/<filename>', methods=['DELETE'])
def deleteCSV(filename):
    """
    Delete a specified CSV file and its properties file.

    Returns:
    Tuple[dict, int]: A JSON response containing a success message and the HTTP status code.

    Status Codes:
        200: Successful deletion of the CSV file and properties file.
        404: File not found (either CSV or properties file).
        500: General server error (any other exceptions
    """
    try: 
        secureFilename =secure_filename(filename)
        filename = os.path.join(current_app.config['csvFolder'], f"{secureFilename}.csv")
        propertiesFileName = os.path.join(current_app.config['csvFolder'], f"{secureFilename}.json")

        os.remove(filename)
        os.remove(propertiesFileName)
        return jsonify(message="Success"), 200
    except FileNotFoundError as e:
        error_message = f"File {filename}.json not found."
        current_app.logger.error(error_message)
        return jsonify({"error": error_message}), 404
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@csvProfilerBP.route('/getCSVColumns/<filename>', methods=['GET'])
def getCSVColumns(filename:str):
    """
    Retrieve the list of columns in a specified CSV file.

    This endpoint loads a CSV file and its properties, retrieves the column names,
    and returns them.

    Parameters:
    filename (str): The name of the CSV file (without extension).

    Returns:
    Tuple[dict, int]: A JSON response containing the list of column names and the HTTP status code.

    Status Codes:
    200: Successful retrieval of column names.
    404: File not found (either CSV or properties file).
    400: Error decoding JSON properties file.
    500: General server error (any other exceptions).

    """
    filename = secure_filename(filename)
    try:
        propertiesFileName = os.path.join(current_app.config['csvFolder'], f"{filename}.json")
        with open(propertiesFileName, 'rb') as properties:
            properties = json.load(properties)

        newCSVProfiler = CSVProfiler(filename, properties)
        newCSVProfiler.loadCSV()
        columns = newCSVProfiler.getColumns()
        return jsonify(columns), 200
    except FileNotFoundError:
        error_message = f"File {filename}.json not found."
        current_app.logger.error(error_message)
        return jsonify({"error": error_message}), 404
    except json.JSONDecodeError:
        error_message = f"Error decoding JSON in file {filename}.json."
        current_app.logger.error(error_message)
        return jsonify({"error": error_message}), 400
    
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@csvProfilerBP.route('/uploadCSV', methods=['POST'])
def csvProfiler():
    
    """
    Upload a CSV file and process it with specified properties.

    This endpoint handles CSV file uploads, validates the form data, and processes the uploaded file
    using the specified properties.

    Returns:
    Tuple[dict, int]: A JSON response containing a success message and the HTTP status code.

    Status Codes:
    200: Successful processing of the CSV file.
    400: Validation error (form data does not meet validation criteria).
    500: General server error (any other exceptions).

    """
    try:
        csvUploadForm = csvUploadSchema()
        data = csvUploadForm.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 400
    try:

        file = request.files['flatDataSet']
        filename, ext = os.path.splitext(file.filename)
        filename = secure_filename(filename)

        delimiter = data.get('csvSeperator', ',')
        headerRow = data.get('headerRow', 0) 
        quotechar = data.get('quoteChar', '"') 

        properties = {
            'delimiter': delimiter,
            'headerRow': headerRow,
            'quotechar': quotechar
        }

        if ext not in current_app.config['ALLOWED_EXTENSIONS']:
            return jsonify({"error": "Invalid file type."}), 400
        elif ext == '.csv':

            newCSVProfiler = CSVProfiler(filename, properties)
            newCSVProfiler.convertToCsv(file)
        else:
            xlsxFile = io.BytesIO(file.read())
            newCSVProfiler = CSVProfiler(filename, properties)
            newCSVProfiler.xlsxToCSV(xlsxFile)
        return jsonify(message="Success"), 200
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500