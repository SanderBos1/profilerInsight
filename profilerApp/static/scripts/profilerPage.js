function getColumns(element) {
    var tableName = element.getAttribute('value');
    var dropdownButton = $('#dropdownMenuButton');
    dropdownButton.text(tableName);

    $.ajax({
        url: 'getColumns/' + tableName,
        type: 'GET',
        success: function(response) {
            // Clear existing content
            $('#ingestButton').empty();
            $('#profilerOverviewContent').empty();
            $('#columnButton').empty();

            // Populate column buttons
            var columnButtons = $('#columnButton');
            for (var i = 0; i < response.columnNames.length; i++) {
                var columnName = response.columnNames[i];
                var buttonHtml = `<button class="btn btn-primary" onclick="getOverview(this)" value="${columnName}">${columnName}</button>`;
                columnButtons.append(buttonHtml);
            }
        },
        error: function(error) {
            console.log('Error fetching columns:', error);
            // Optionally show an error message to the user
            alert('Error fetching columns. Please try again.');
        }
    });
}



function DisplayOverview(response){
    $('#profilerOverviewContent').empty()
    var displayProfilerBasics = $('#profilerOverviewContent');
    
    rowCount = document.createElement("p")
    uniqueValuesCount = document.createElement("p")
    nanCount = document.createElement("p")
    columType = document.createElement("p")

    var rowCount = $('<p>').text("Number of rows: " + response.rowCount);
    var uniqueValuesCount = $('<p>').text("Unique values: " + response.distinctValues);
    var nanCount = $('<p>').text("Total missing values: " + response.nanValues);
    var columnType = $('<p>').text("Column type: " + response.columnType);

    displayProfilerBasics.append(rowCount, uniqueValuesCount, nanCount, columnType);
}


function getOverview(button){
    ingestButtonDiv = $('#ingestButtonDiv')
    ingestButtonDiv.empty()

    var ingestButton = $('<button>').text("Ingest Data")
    .val(button.value)
    .addClass("btn btn-primary")
    .click(function() {
        ingestData(this);
    });
    ingestButtonDiv.append(ingestButton);

    $.ajax({
        url: '/getOverview/' + button.value,
        type: 'GET',
        success: function(response){

            if( response != "No ingestion was done"){
                DisplayOverview(response)
            }
            else{
                var displayProfilerBasics = $('#profilerOverviewContent');
                displayProfilerBasics.empty();
                displayProfilerBasics.text("No ingestion was done");

            }

        },
        error: function(error){
            console.log(error);
        }
    })
};
    

function ingestData(button){
    $.ajax({
        url: '/ingest/' + button.value,
        type: 'GET',
        success: function(response){
            DisplayOverview(response)

        },
        error: function(error){
            console.log(error);
        }
    })
};
