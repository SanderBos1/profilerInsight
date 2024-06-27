function getOverview(button){
    console.log(button)
    console.log(button.value)
    var tableName = {
        'tableName': button.value
    }
    var tableNameJson = JSON.stringify(tableName)
    $.ajax({
        url: 'getOverview',
        type: 'POST',
        contentType: 'application/json',
        data: tableNameJson,
        success: function(response){
            console.log(response)
            displayRowCount = document.getElementById('rowCount')
            displayRowCount.innerHTML = response['rowCount']
        },
        error: function(error){
            console.log(error);
        }
    });
}