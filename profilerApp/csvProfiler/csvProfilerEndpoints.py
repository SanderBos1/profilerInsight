from flask import Blueprint, jsonify
from ..csvProfiler.forms import UploadForm
from ..csvProfiler.csvProfiler import csvProfilerClass

csvProfilerBP = Blueprint(
    "csvProfilerBP",
    __name__,
)


@csvProfilerBP.route('/csvProfiler', methods=['POST'])
def csvProfiler():
    form = UploadForm()
    if form.validate_on_submit():
        try:
            seperator = form.csvSeperator.data
            file = form.csvFile.data
            header = form.headerRow.data
            quotechar = form.quoteChar.data
            newCsvProfiler = csvProfilerClass(file, seperator, header, quotechar)
            columnValues = newCsvProfiler.csvStandardProfiler() 
            return columnValues, 200
        except Exception as e:
            return str(e), 500
    else:
        return jsonify("form not validated"), 500