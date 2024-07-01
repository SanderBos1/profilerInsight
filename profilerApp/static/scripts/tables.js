$(document).ready(function() {
    const apiEndpoint = '/getTables'; // Replace with your actual API endpoint

    // Function to fetch and display data
    function fetchConnections() {
        fetch(apiEndpoint)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                // Reference to the table body
                const tableBody = $('#connectionTable tbody');
                // Clear existing data
                tableBody.empty();
                // Populate the table with new data
                data.forEach(table => {
                    const row = `
                        <tr>
                            <td>${table['uniqueTableName']}</td>
                            <td>${table['connectionId']}</td>
                            <td>${table['schema']}</td>
                            <td>${table['table']}</td>
                            <td><button class="btn btn-danger" type="button" name="remove" onclick="deleteRow(this)">Remove</button></td>
                        </tr>
                    `;
                    tableBody.append(row);
                });
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                alert('Failed to fetch connections. Please try again.');
            });
    }

    // Fetch and display data on page load
    fetchConnections();
});

$(document).ready(function() {
    $('#addTableForm').submit(function (e) {

        let formData = convertFormToJSON($(this));
        let csrfToken = getCsrfToken();

        $.ajax({
            type: "POST",
            url: "/addTable",
            headers: {
                'X-CSRFToken': csrfToken
            },
            contentType: 'application/json',
            data: formData, 
            success: function (data) {
                const tableBody = $('#connectionTable tbody');
                const row = `
                    <tr>
                        <td>${data.uniqueTableName}</td>
                        <td>${data.connectionId}</td>
                        <td>${data.schema}</td>
                        <td>${data.table}</td>
                        <td><button class="btn btn-danger" type="button" name="remove" onclick="deleteRow(this)">Remove</button></td>
                    </tr>
                    `;
                    tableBody.append(row);
                },
        error: function(error) {
            console.error('Error:', error);
            alert('Failed to add table. Please try again.');         
        }
        });
        e.preventDefault();
    });
});

function deleteRow(button){
    const csrfToken = getCsrfToken();
    const tableRow = button.closest('tr'); // Using closest for better readability
    const uniqueTableName = $(tableRow).find('td').eq(0).text(); // Using jQuery for consistency

    const dataOBJ = {
        "uniqueTableName": uniqueTableName
    };
    const dataOBJJson = JSON.stringify(dataOBJ);

    $.ajax({
        url: '/deleteTable',
        type: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken
        },
        contentType: 'application/json',
        data: dataOBJJson,
        success: function() {
            $(tableRow).remove(); // Use jQuery to remove the row for consistency
        },
        error: function(error) {
            console.error('Error:', error);
            alert('Failed to delete table. Please try again.'); // Provide feedback to the user
        }
    });
}