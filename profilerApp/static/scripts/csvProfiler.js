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
                displayCsvProfilerData(response, csvProfilerHolder);
            },
            error: function(error){
                console.log(error);
                alert('Failed to process the CSV file. Please try again.');
            }
        });
    });

    function displayCsvProfilerData(data, container) {
        data.forEach(function(column) {
            var columnInfo = createColumnInfo(column);
            container.append(columnInfo);
        });
    }

    function createColumnInfo(column) {

        var columnInfo = $('<div>').addClass('col-md-4 column-info');
        var card = $('<div>').addClass('card');
        var cardBody = $('<div>').addClass('card-body');

        var columnName = $('<h3>').text(`Column Name: ${column.columnName}`);
        var columnType = $('<p>').text(`Column Type: ${column.columnType}`);
        var lenColumn = $('<p>').text(`Column Length: ${column.lenColumn}`);
        var distinctValues  = $('<p>').text(`Distinct Values: ${column.distinctValues}`);
        var uniqueValues  = $('<p>').text(`Unique Values: ${column.uniqueValues}`);
        var nanValues = $('<p>').text(`NaN Values: ${column.nanValues} %`);
        var mean = $('<p>').text(`Mean: ${column.meanColumn}`);
        var min = $('<p>').text(`Min: ${column.minColumn}`);
        var max = $('<p>').text(`Max: ${column.maxColumn}`);

        cardBody.append(columnName, columnType, lenColumn, distinctValues, uniqueValues, nanValues, mean, min, max);
        card.append(cardBody);
        columnInfo.append(card);

        return columnInfo;
    }
});