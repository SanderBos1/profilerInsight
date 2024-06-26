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
                    console.log(connection)
                    const row = `
                        <tr>
                            <td>${connection['Host']}</td>
                            <td>${connection['Port']}</td>
                            <td>${connection['DataBase']}</td>
                            <td>${connection['UserName']}</td>
                            <td>${connection['Password']}</td>
                            <td>${connection['DatabaseType']}</td>

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



$('#addConnectionForm').submit(function(event) {

    // Serialize form data into a query string
    var formData = new FormData(this);
    var formDataObj = {};
    formData.forEach(function(value, key) {
        formDataObj[key] = value;
    });
    var connection = JSON.stringify(formDataObj);
    $.ajax({
        url: '/addConnection',  // Replace with your server endpoint
        type: 'POST',
        contentType: 'application/json',
        data: connection,
        success: function(response) {
            console.log('Success:', response);
        },
        error: function(error) {
            console.error('Error:', error);
            // Optionally, handle error
        }
    });

});