document.addEventListener("DOMContentLoaded", function() {
    // API endpoint URL
    const apiEndpoint = 'http://127.0.0.1:5000/getTables';

    // Function to fetch and display data
    function fetchConnections() {
        fetch(apiEndpoint)
            .then(response => response.json())
            .then(data => {
                // Reference to the table body
                const tableBody = document.querySelector('#connectionTable tbody');
                // Clear existing data
                tableBody.innerHTML = '';
                // Populate the table with new data
                data.forEach(table => {
                    const row = `
                        <tr>
                            <td>${table['uniqueTableName']}</td>
                            <td>${table['connectionId']}</td>
                            <td>${table['schema']}</td>
                            <td>${table['table']}</td>
                            <td><button class="btn" type="button" name="remove"  onclick="deleteRow(this)">Remove</button></td>
                        </tr>
                    `;
                    tableBody.insertAdjacentHTML('beforeend', row);
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    // Fetch and display data on page load
    fetchConnections();
});

$(document).ready(function() {
    $('#addTableForm').submit(function (e) {
        formData = convertFormToJSON($(this));
        var csrfToken = getCsrfToken();
        $.ajax({
            type: "POST",
            url: "/addTable",
            headers: {
                'X-CSRFToken': csrfToken
            },
            contentType: 'application/json',
            data: formData, 
            success: function (data) {
                const tableBody = document.querySelector('#connectionTable tbody');
                const row = `
                        <tr>
                            <td>${data['uniqueTableName']}</td>
                            <td>${data['connectionId']}</td>
                            <td>${data['schema']}</td>
                            <td>${data['table']}</td>
                            <td><button class="btn" type="button" name="remove"  onclick="deleteRow(this)">Remove</button></td>
                        </tr>
                    `;
                    tableBody.insertAdjacentHTML('beforeend', row);
            },
        error: function(error) {
            console.error('Error:', error);
        }
        });
        e.preventDefault();
    });
});

function deleteRow(button){
    var csrfToken = getCsrfToken();
    var tableRow=button.parentNode.parentNode;
    var rowIndex = tableRow.rowIndex
    cells = tableRow.getElementsByTagName('td');
    uniqueTableName = cells[0].innerHTML
    dataOBJ = {
                "uniqueTableName": uniqueTableName,
            }   
    dataOBJJson = JSON.stringify(dataOBJ)
    $.ajax({
        url: '/deleteTable',  
        type: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
        },
        contentType: 'application/json',
        data: dataOBJJson,
        success: function(response) {
            document.getElementById('connectionTable').deleteRow(rowIndex);
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });



};