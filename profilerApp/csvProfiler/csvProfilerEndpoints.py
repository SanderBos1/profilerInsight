from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from .jsonSchemas import csvUploadSchema
from ..csvProfiler.csvProfiler import csvProfilerClass

csvProfilerBP = Blueprint(
    "csvProfilerBP",
    __name__,
)


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
@csvProfilerBP.route('/csvProfiler', methods=['POST'])
def csvProfiler():
    try:
        csvUploadForm = csvUploadSchema()
        data = csvUploadForm.load(request.form)
    except ValidationError as e:
        return jsonify(e.messages), 400
    # try:
    seperator = data.get('csvSeperator', ',')
    file = request.files['csvFile']
    header = data.get('headerRow', 0) 
    quotechar = data.get('quoteChar', '"') 
    newCsvProfiler = csvProfilerClass(file, seperator, header, quotechar)
    columnValues = newCsvProfiler.csvStandardProfiler() 
    return jsonify(columnValues), 200
    # except Exception as e:
    #     return str(e), 500
