function getColumns(button){
    var tableName = button.value
    console.log(tableName)
    console.log(typeof(tableName))
    $.ajax({
        url: 'getColumns/' + tableName,
        type: 'GET',
        success: function(response){
            displayProfilerBasics = document.getElementById('Overview')
            displayProfilerBasics.innerHTML = ''
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
    $.ajax({
        url: '/getOverview/' + button.value,
        type: 'GET',
        success: function(response){
            displayProfilerBasics = document.getElementById('Overview')
            displayProfilerBasics.innerHTML = ''
            rowCount = document.createElement("p")
            uniqueValuesCount = document.createElement("p")
            nanCount = document.createElement("p")
            columType = document.createElement("p")

            rowCount.innerText = "Number of rows: " + response['rowCount']
            uniqueValuesCount.innerText = "Unique values: " + response['distinctValues']
            nanCount.innerText = "Total missing values: " + response['nanValues']
            columType.innerText = "Column type: " + response['columnType']

            displayProfilerBasics.appendChild(rowCount)
            displayProfilerBasics.appendChild(uniqueValuesCount)
            displayProfilerBasics.appendChild(nanCount)
            displayProfilerBasics.appendChild(columType)

        },
        error: function(error){
            console.log(error);
        }
    });
}