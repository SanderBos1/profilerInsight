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
                    console.log(table)

                    const row = `
                        <tr>
                            <td>${data['uniqueTableName']}</td>
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
        $.ajax({
            type: "POST",
            url: "/addTable",
            contentType: 'application/json',
            data: formData, // serializes the form's elements.
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
            }
        });
        e.preventDefault(); // block the traditional submission of the form.
    });

    // Inject our CSRF token into our AJAX request.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    })
});

function deleteRow(button){
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
        type: 'POST',
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