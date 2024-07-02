from flask import Blueprint, request, jsonify
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
            file = form.csvFile.data
            newCsvProfiler = csvProfilerClass(file)
            columnValues = newCsvProfiler.csvStandardProfiler() 
            return columnValues, 200
        except Exception as e:
            return str(e), 500
    else:
        return jsonify("form not validated"), 500