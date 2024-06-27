document.addEventListener("DOMContentLoaded", function() {
    // API endpoint URL
    const apiEndpoint = 'http://127.0.0.1:5000/getConnections';

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
                data.forEach(connection => {
                    const row = `
                        <tr>
                            <td>${connection['connectionID']}</td>
                            <td>${connection['host']}</td>
                            <td>${connection['port']}</td>
                            <td>${connection['username']}</td>
                            <td>*****</td>
                            <td>${connection['database']}</td>
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
    $('#addConnectionForm').submit(function (e) {
        formData = convertFormToJSON($(this));
        $.ajax({
            type: "POST",
            url: "/addConnection",
            contentType: 'application/json',
            data: formData, // serializes the form's elements.
            success: function (data) {
                const tableBody = document.querySelector('#connectionTable tbody');
                const row = `
                        <tr>
                            <td>${data['connectionId']}</td>
                            <td>${data['host']}</td>
                            <td>${data['port']}</td>
                            <td>${data['username']}</td>
                            <td>*****</td>
                            <td>${data['database']}</td>
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
    connectionId = cells[0].innerHTML
    dataOBJ = {"connectionId": connectionId}
    connectionIdJson = JSON.stringify(dataOBJ)
    $.ajax({
        url: '/deleteTable',  // Replace with your server endpoint
        type: 'POST',
        contentType: 'application/json',

        data: connectionIdJson,
        success: function(response) {
            document.getElementById('connectionTable').deleteRow(rowIndex);
        },
        error: function(error) {
            console.error('Error:', error);
            // Optionally, handle error
        }
    });



};