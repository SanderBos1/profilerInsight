$(document).ready(function() {
    $('#csvForm').submit(function (e) {
        e.preventDefault();

        var formData = new FormData($('#csvForm')[0]);
        var csrfToken = getCsrfToken();
        var csvProfilerHolder = $('#csvProfilerData');
        csvProfilerHolder.empty();

        $.ajax({
            type: "POST",
            url: "/csvProfiler",
            headers: {
                'X-CSRFToken': csrfToken
            },
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (response) {
                response.forEach(function(column) {
                    createColumnInfo(csvProfilerHolder, column)
             })},
            error: function(error){
                console.log(error);
                alert('Failed to process the CSV file. Please try again.');
            }
        });
    });


function createColumnInfo(csvProfilerHolder, column) {

    var template = $('#templateCsvColumn').contents().clone(true);

    // Populate template with column data
    template.find('.columnName').text(column.columnName);
    template.find('.columnType').text(column.columnType);
    template.find('.columnLength').text(column.lenColumn);
    template.find('.uniqueValues').text(column.uniqueValues);
    template.find('.nanValues').text(column.nanValues);
    template.find('.nanValues').attr('aria-valuenow', column.nanValues);
    template.find('.progress-bar').css('width', column.nanValues + '%');
    template.find('.averageValue').text('Mean: ' + column.meanColumn);
    template.find('.minValue').text('Min: ' + column.minColumn);
    template.find('.maxValue').text('Max: ' + column.maxColumn);

    // Append template to csvProfilerHolder
    csvProfilerHolder.append(template);
    }
});