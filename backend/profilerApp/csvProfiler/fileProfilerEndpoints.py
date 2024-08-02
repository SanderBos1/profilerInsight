from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
import os
import json
from .jsonSchemas import csvUploadSchema
from .FlatFileHandler import FlatFileHandler
from .profilerGenerator import profilerGenerator
import io
from flasgger import swag_from

csvProfilerBP = Blueprint(
    "csvProfilerBP",
    __name__,
)

@csvProfilerBP.route('/getColumnOverview/<filename>/<column>', methods=['GET'])
@swag_from({    'tags': ['File Profiler'],
    'description': 'Retrieve the overview of a specific column in a CSV file.',
    'parameters': [
        {
            'name': 'filename',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The name of the CSV file (without extension).'
        },
        {
            'name': 'column',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The name of the column to profile.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful retrieval of column profiling information',
            'schema': {
                'type': 'object',
                'properties': {
                    'columnName': {'type': 'string'},
                    'columnType': {'type': 'string'},
                    'lenColumn': {'type': 'integer'},
                    'distinctValues': {'type': 'integer'},
                    'uniqueValues': {'type': 'integer'},
                    'nanValues': {'type': 'number'},
                    'baseStats': {
                        'type': 'object',
                        'properties': {
                            'meanColumn': {'type': 'string'},
                            'medianColumn': {'type': 'string'},
                            'minColumn': {'type': 'string'},
                            'maxColumn': {'type': 'string'}
                        }
                    },
                    'numericImages': {
                        'type': 'object',
                        'properties': {
                            'histogram': {'type': 'string'},
                            'boxplot': {'type': 'string'}
                        }
                    },
                    'dataPreview': {'type': 'string'}
                }
            }
        },
        '404': {
            'description': 'File not found (either CSV or properties file).'
        },
        '400': {
            'description': 'Error decoding JSON properties file.'
        },
        '500': {
            'description': 'General server error (any other exceptions).'
        }
    }})
def getColumnOverview(filename:str, column:str):
    filename = secure_filename(filename)
    try:
        profiler_generator = profilerGenerator(filename)
        columns = profiler_generator.fileProfiler(column)
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
@swag_from({
    'tags': ['File Profiler'],  
    'description': 'Retrieve a list of all CSV files in the configured directory. This endpoint scans the configured directory for CSV files and returns their filenames without extensions.',
    'responses': {
        '200': {
            'description': 'Successful retrieval of CSV filenames',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'description': 'A list of CSV filenames without extensions'
                }
            }
        },
        '500': {
            'description': 'General server error (any other exceptions)'
        }
    }
})
def getCSVFiles():
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
@swag_from({
    'tags': ['File Profiler'],
    'description': 'Delete a specified CSV file and its properties file.',
    'parameters': [
        {
            'name': 'filename',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The name of the CSV file to be deleted (without extension).'
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful deletion of the CSV file and properties file.',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Success message'
                    }
                }
            }
        },
        '404': {
            'description': 'File not found (either CSV or properties file).'
        },
        '500': {
            'description': 'General server error (any other exceptions).'
        }
    }
})
def deleteCSV(filename):
    try: 
        sec_filename =secure_filename(filename)
        filename = os.path.join(current_app.config['csvFolder'], f"{sec_filename}.csv")
        properties_filename = os.path.join(current_app.config['csvFolder'], f"{sec_filename}.json")
        os.remove(filename)
        os.remove(properties_filename)
        return jsonify(message="Success"), 200
    except FileNotFoundError as e:
        error_message = f"File {filename}.json not found."
        current_app.logger.error(error_message)
        return jsonify({"error": error_message}), 404
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@csvProfilerBP.route('/getCSVColumns/<filename>', methods=['GET'])
@swag_from({
    'tags': ['File Profiler'],
    'description': 'Retrieve the list of columns in a specified CSV file. This endpoint loads a CSV file and its properties, retrieves the column names, and returns them.',
    'parameters': [
        {
            'name': 'filename',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The name of the CSV file (without extension) to retrieve column names from.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful retrieval of column names.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'description': 'A list of column names in the CSV file.'
                }
            }
        },
        '404': {
            'description': 'File not found (either CSV or properties file).'
        },
        '400': {
            'description': 'Error decoding JSON properties file.'
        },
        '500': {
            'description': 'General server error (any other exceptions).'
        }
    }
})
def getCSVColumns(filename:str):
    filename = secure_filename(filename)
    try:
        profiler_generator = profilerGenerator(filename)
        columns = profiler_generator.getColumns()
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
@swag_from({
    'tags': ['File Profiler'],
    'description': 'Upload a  file and process it with specified properties. This endpoint handles file uploads, validates the form data, and processes the uploaded file using the specified properties.',
    'parameters': [
        {
            'name': 'flatDataSet',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'The CSV file to be uploaded and processed.'
        },
        {
            'name': 'csvSeperator',
            'in': 'formData',
            'type': 'string',
            'default': ',',
            'description': 'The delimiter used in the CSV file.'
        },
        {
            'name': 'headerRow',
            'in': 'formData',
            'type': 'integer',
            'default': 0,
            'description': 'The row number (0-based index) that contains the header information.'
        },
        {
            'name': 'quoteChar',
            'in': 'formData',
            'type': 'string',
            'default': '"',
            'description': 'The character used to quote fields in the CSV file.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Successful processing of the CSV file.',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Success'
                    }
                }
            }
        },
        '400': {
            'description': 'Validation error (form data does not meet validation criteria).'
        },
        '500': {
            'description': 'General server error (any other exceptions).'
        }
    }
})
def csvProfiler():
    try:
        csv_upload_form = csvUploadSchema()
        data = csv_upload_form.load(request.form)
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
            flat_file_handler = FlatFileHandler(filename, properties)
            flat_file_handler.uploadCSV(file)
        else:
            xlsx_file = io.BytesIO(file.read())
            flat_file_handler = FlatFileHandler(filename, properties)
            flat_file_handler.uploadXLSX(xlsx_file)
        return jsonify(message="Success"), 200
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500