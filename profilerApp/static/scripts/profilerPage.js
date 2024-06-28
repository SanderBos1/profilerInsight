function getColumns(button){
    var tableName = {
        'tableName': button.value
    }
    var tableNameJson = JSON.stringify(tableName)
    $.ajax({
        url: 'getColumns',
        type: 'POST',
        contentType: 'application/json',
        data: tableNameJson,
        success: function(response){
            columnButtons = document.getElementById('columnButton')
            columnButtons.innerHTML = ''
            for (var i = 0; i < response['columnNames'].length; i++){

                columnButtons.innerHTML += '<button class="btn btn-primary" onclick="getOverview(this)" value="' + response['columnNames'][i] + '">' + response['columnNames'][i] + '</button>'
            }
        },
        error: function(error){
            console.log(error);
        }
    });
}


function getOverview(button){
    var tableName = {
        'columName': button.value
    }
    var tableNameJson = JSON.stringify(tableName)
    $.ajax({
        url: '/getOverview',
        type: 'POST',
        contentType: 'application/json',
        data: tableNameJson,
        success: function(response){
            displayRowCount = document.getElementById('Overview')
            displayRowCount.innerHTML = ''
            rowCount = document.createElement("p")
            uniqueValuesCount = document.createElement("p")
            nanCount = document.createElement("p")

            rowCount.innerText = "Number of rows: " + response['rowCount']
            uniqueValuesCount.innerText = "Unique values: " + response['distinctValues']
            nanCount.innerText = "Total missing values: " + response['nanValues']

            displayRowCount.appendChild(rowCount)
            displayRowCount.appendChild(uniqueValuesCount)
            displayRowCount.appendChild(nanCount)

        },
        error: function(error){
            console.log(error);
        }
    });
}