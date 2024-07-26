from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from marshmallow import ValidationError
import os
import json
from .jsonSchemas import csvUploadSchema
from ..csvProfiler.csvProfiler import CSVProfiler

csvProfilerBP = Blueprint(
    "csvProfilerBP",
    __name__,
)

@csvProfilerBP.route('/getColumnOverview/<filename>/<column>', methods=['GET'])
def getColumnOverview(filename, column):
    filename = secure_filename(filename)
    try:
        fullFilename = os.path.join(current_app.config['csvFolder'], f"{filename}.csv")
        with open(fullFilename, 'r', encoding='utf-8') as file:
            file = file.read()

        propertiesFileName = os.path.join(current_app.config['csvFolder'], f"{filename}.json")
        with open(propertiesFileName, 'rb') as properties:
            properties = json.load(properties)

        newcsv = CSVProfiler(file, properties)
        columns = newcsv.csvStandardProfiler(column)

        return jsonify(columns), 200
    except Exception as e:
        return jsonify(str(e)), 500


@csvProfilerBP.route('/getCSVFiles', methods=['GET'])
def getCSVFiles():
    files = os.listdir(current_app.config['csvFolder'])
    filenames = []
    for file in files:
        filename = file.split(".")
        if filename[1] == "csv":
            filenames.append(filename[0])
    return jsonify(filenames), 200

@csvProfilerBP.route('/getCSVColumns/<filename>', methods=['GET'])
def getCSVColumns(filename):
    filename = secure_filename(filename)
    try:
        fullFilename = os.path.join(current_app.config['csvFolder'], f"{filename}.csv")
        with open(fullFilename, 'r', encoding='utf-8') as file:
            file = file.read()

        propertiesFileName = os.path.join(current_app.config['csvFolder'], f"{filename}.json")
        with open(propertiesFileName, 'rb') as properties:
            properties = json.load(properties)

        newcsv = CSVProfiler(file, properties)
        newcsv.convertToCsv()
        columns = newcsv.getColumns()

        return jsonify(columns), 200
    except Exception as e:
        return jsonify(str(e)), 500


"""
Input:
    Content Type: multipart/form-data
    Required Fields:
        csvFile: The CSV file to be processed (type: file).
    Optional Fields:
    csvSeperator: (str) The delimiter used in the CSV file. Default is ','.
    headerRow: (int) The index of the header row in the CSV file. Default is 0.
    quoteChar: (str) The character used to quote fields in the CSV file. Default is '"'.
    
    Goal: read the basic information of the csv file and return the column names and their basic statistics

    output: a JSON object with a list of column names and their corresponding statistics

    status codes:
        200:  The file was read and processed successfully.
        400: The input JSON object is invalid. This includes missing required fields or invalid data types.
        500: An error occurred while reading the CSV file. This could be due to file reading issues, parsing errors, or other unexpected conditions.

"""

@csvProfilerBP.route('/uploadCSV', methods=['POST'])
def csvProfiler():
    try:
        csvUploadForm = csvUploadSchema()
        data = csvUploadForm.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 400
    try:

        separator = data.get('csvSeperator', ',')
        file = request.files['csvFile']
        filename, ext = os.path.splitext(file.filename)
        csvFileName = current_app.config['csvFolder'] + filename + ".csv"
        headerRow = data.get('headerRow', 0) 
        quotechar = data.get('quoteChar', '"') 

        file.save(csvFileName)
        properties = {
            'separator': separator,
            'headerRow': headerRow,
            'quotechar': quotechar
        }
        propertiesJson = json.dumps(properties)
        propertiesFilePath = current_app.config['csvFolder'] + filename + ".json"
        with open(propertiesFilePath, 'w') as jsonFile:
            jsonFile.write(propertiesJson)
        return jsonify(message="Success"), 200
    except Exception as e:
        return str(e), 500
