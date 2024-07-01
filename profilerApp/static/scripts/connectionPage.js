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
                            <td>${connection['connectionId']}</td>
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
        var csrfToken = getCsrfToken();
        $.ajax({
            type: "POST",
            url: "/addPostgresqlConnection",
            headers: {
                'X-CSRFToken': csrfToken
            },
            contentType: 'application/json',
            data: formData, // serializes the form's elements.
            success: function (data) {
                const tableBody = $('#connectionTable tbody');
                const row = `
                        <tr>
                            <td>${data.connectionId}</td>
                            <td>${data.host}</td>
                            <td>${data.port}</td>
                            <td>${data.username}</td>
                            <td>*****</td>
                            <td>${data.database}</td>
                            <td><button class="btn" type="button" name="remove"  onclick="deleteRow(this)">Remove</button></td>
                        </tr>
                    `;
                tableBody.append(row);
            },
            error: function(error){
                console.log(error);
                alert('Failed to add connection. Please try again.');
            }

            });
            e.preventDefault(); // block the traditional submission of the form.
        });
    });


    function deleteRow(button) {
        const tableRow = button.closest('tr');
        const connectionId = $(tableRow).find('td').eq(0).text();
        const dataOBJ = { "connectionId": connectionId };
        const connectionIdJson = JSON.stringify(dataOBJ);
        const csrfToken = getCsrfToken();
        $.ajax({
            url: '/deleteConnection',
            headers: {
                'X-CSRFToken': csrfToken
            },
            type: 'DELETE',
            contentType: 'application/json',
            data: connectionIdJson,
            success: function(response) {
                $(tableRow).remove(); // Use jQuery to remove the row
            },
            error: function(error) {
                console.error('Error:', error);
                alert('Failed to delete connection. Please try again.'); // Provide feedback to the user
            }
        });
    }