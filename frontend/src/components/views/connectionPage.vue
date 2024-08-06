<template>
    <div class="row mt-3">
        <div class="offset-md-10">
            <button class="btn btn-secondary" @click="showModal = true" data-bs-toggle="tooltip" title="Define a connection to a database" >Add Connection</button>    
        </div>
    </div>
    
    <div class="row mt-3">
        <div class="col-md-12">
            <table class="table" id="connectionTable">
                <thead class="thead-dark">
                    <tr>
                        <th scope="col">Connection ID</th>
                        <th scope="col">Host</th>
                        <th scope="col">Port</th>
                        <th scope="col">Username</th>
                        <th scope="col">Password</th>
                        <th scope="col">Database</th>
                        <th scope="col">db_type</th>

                    </tr>
                </thead>
                <tbody> 
                    <tr v-for="connection in connections" :key="connection.connectionId">
                        <td>{{ connection.connection_id }}</td>
                        <td>{{ connection.host }}</td>
                        <td>{{ connection.port }}</td>
                        <td>{{ connection.username }}</td>
                        <td>*****</td> <!-- You should not display passwords directly in UI -->
                        <td>{{ connection.database }}</td>
                        <td>{{ connection.db_type}}</td>
                        <td><button class="btn btn-primary grey" @click="deleteConnection(connection.connection_id)" data-bs-toggle="tooltip" title="Removes the connection, and everything connected to it.">Remove</button></td>
                    </tr>      
            </tbody>
            </table>
        </div>
    </div>
    <basicDialogue :visible="errorVisible"  @update:visible="errorVisible = $event" dialogTitle="csv Upload Error">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    {{connectionError }}
                </div>
            </template>
    </basicDialogue>
    <basicDialogue :visible="showModal" @update:visible="showModal = $event" dialogTitle="Choose Connection Type">
        <template v-slot:dialogueBody>
            <div class="row">
                <div class="col-4">
                    <img src="../../assets/Images/postgresLogo.jpg" @click="changeModals()" class="img-thumbnail" alt="Postgres Logo">
                </div>
            </div>
        </template>
    </basicDialogue>

    <basicDialogue :visible="showPostgres"  @update:visible="showPostgres = $event" dialogTitle="Postgres Connection">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    <form v-on:submit.prevent="submitPostgressForm" id="addConnectionForm">
                        <div class="mb-3">
                            <label for="connectionId" class="form-label">Connection ID</label>
                            <input type="text" id="connectionId"  v-model="postgresConnectionForm.connection_id" class="form-control" data-bs-toggle="tooltip" title="A unique identifier of your connections">
                        </div>
                    <div class="mb-3">
                        <label for="host" class="form-label">Host</label>
                        <input type="text" id="host" v-model="postgresConnectionForm.host" class="form-control" data-bs-toggle="tooltip" title="Where your database is hosted">
                    </div>
                    <div class="mb-3">
                        <label for="port" class="form-label">Port</label>
                        <input type="text" id="port" v-model="postgresConnectionForm.port" class="form-control" data-bs-toggle="tooltip" title="The port of your database server">
                    </div>
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" id="username" v-model="postgresConnectionForm.username" class="form-control" data-bs-toggle="tooltip" title="The user that connects to the databgase">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" id="password" v-model="postgresConnectionForm.password" class="form-control" data-bs-toggle="tooltip" title="The corresponding password">
                    </div>
                    <div class="mb-3">
                        <label for="database" class="form-label">Database</label>
                        <input type="text" id="database" v-model="postgresConnectionForm.database" class="form-control" data-bs-toggle="tooltip" title="Which database you want to connect to.">
                    </div>        
                    <div class="mb-3">
                        <label for="db_type" class="form-label">db_type</label>
                        <input type="text" id="db_type" v-model="postgresConnectionForm.db_type" class="form-control" readonly data-bs-toggle="tooltip" title="Your chosen Database Type">
                    </div>  
                        <button class="btn btn-primary grey">Submit</button>
                    </form>
                </div>
            </template>
            <template v-slot:dialogueFooter>
                <button class="btn btn-primary grey" @click="changeModals()">Return</button>

            </template>

    </basicDialogue>
</template>

<script>
import basicDialogue  from '../baseDialogue.vue'


const API_ENDPOINTS = {
  GET_CONNECTIONS: 'http://127.0.0.1:5000/get_connections',
  ADD_POSTGRES_CONNECTION: 'http://127.0.0.1:5000/add_postgres_connection',
  DELETE_CONNECTION: connection_id => `http://127.0.0.1:5000/delete_connection/${connection_id}`,
  ingest_connection_tables: 'http://127.0.0.1:5000/ingest_connected_tables'

};


export default {
    name: 'tablePage',
    components:{
        basicDialogue
    },
    data() {
        return {
        errorVisible: false,
        connectionError: "",
        showModal: false,
        showPostgres: false,
        connections: [],
        postgresConnectionForm:{
            connection_id: "",
            host: "",
            port: "",
            username: "",
            password: "",
            database: "",
            db_type: "postgres"
        }
    };
  },
  created() {
    this.fetchConnections();
  },
  methods: {
    async fetchData(url, method) {
        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) {
                const data = await response.json();
                const errorMessage = data.error
                this.handleError(`${response.status}, ${errorMessage}`);
                return null; 
            }   
            return await response.json();
        }catch (error) {
            this.handleError(error.message);
        }
    },
    handleError(message) {
        this.errorVisible = true;
        this.connectionError = message;
    },

    async fetchConnections() {
      const apiEndpoint = API_ENDPOINTS.GET_CONNECTIONS;
      await this.fetchData(apiEndpoint, 'GET')
        .then((data) => {
          if (data) {
            this.connections = data;
          }
        });
    },
    async submitPostgressForm() {
    try {
        const response = await fetch("http://127.0.0.1:5000/add_postgres_connection", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(this.postgresConnectionForm)
        });

        if (!response.ok) {
            this.errorVisible = true;
            this.tabelError = response.status;
        }
        else{
            this.fetchConnections()
            this.ingestTables()
            this.showPostgres = false;
            }
        
    } catch (error) {
        this.errorVisible = true;
        this.tabelError = error;
    }
    },
    async deleteConnection(connection_id) {
        const apiEndpoint = API_ENDPOINTS.DELETE_CONNECTION(connection_id);
        await this.fetchData(apiEndpoint, 'DELETE');
        this.fetchConnections();

    },
    async ingestTables(){
        const apiEndpoint = API_ENDPOINTS.ingest_connection_tables;
        await this.fetchData(apiEndpoint, 'GET');
    },
    changeModals(){
        this.showModal = !this.showModal;
        this.showPostgres = !this.showPostgres;
    },
}};
    
</script>