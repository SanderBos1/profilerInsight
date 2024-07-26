<template>
    <div class="row mt-3">
        <div class="offset-md-10">
            <button class="btn btn-secondary" @click="showModal = true" >Add Connection</button>    
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
                    </tr>
                </thead>
                <tbody> 
                    <tr v-for="connection in connections" :key="connection.connectionId">
                        <td>{{ connection.connectionId }}</td>
                        <td>{{ connection.host }}</td>
                        <td>{{ connection.port }}</td>
                        <td>{{ connection.username }}</td>
                        <td>*****</td> <!-- You should not display passwords directly in UI -->
                        <td>{{ connection.database }}</td>
                        <td><button class="btn" @click="deleteConnection(connection)">Remove</button></td>
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
                    <img src="../assets/Images/postgresLogo.jpg" @click="changeModals()" class="img-thumbnail" alt="Postgres Logo">
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
                            <input type="text" id="connectionId"  v-model="postgresConnectionForm.connectionId" class="form-control">
                        </div>
                    <div class="mb-3">
                        <label for="host" class="form-label">Host</label>
                        <input type="text" id="host" v-model="postgresConnectionForm.host" class="form-control">
                    </div>
                    <div class="mb-3">
                        <label for="port" class="form-label">Port</label>
                        <input type="text" id="port" v-model="postgresConnectionForm.port" class="form-control">
                    </div>
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" id="username" v-model="postgresConnectionForm.username" class="form-control">
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" id="password" v-model="postgresConnectionForm.password" class="form-control">
                    </div>
                    <div class="mb-3">
                        <label for="database" class="form-label">Database</label>
                        <input type="text" id="database" v-model="postgresConnectionForm.database" class="form-control">
                    </div>
                        <button class="btn btn-primary">Submit</button>
                    </form>
                </div>
            </template>
            <template v-slot:dialogueFooter>
                <button class="btn btn-primary" @click="changeModals()">Return</button>

            </template>

    </basicDialogue>
</template>

<script>
import basicDialogue  from './baseDialogue.vue'

export default {
    name: 'connectionTable',
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
            connectionId: "",
            host: "",
            port: "",
            username: "",
            password: "",
            database: ""
        }
    };
  },
  created() {
    // Fetch data when component is created
    this.fetchConnections();
  },
  methods: {
    changeModals(){
        this.showModal = !this.showModal;
        this.showPostgres = !this.showPostgres;
    },
    fetchConnections() {
      const apiEndpoint = 'http://127.0.0.1:5000/getConnections';
      fetch(apiEndpoint)
        .then(response => response.json())
        .then(data => {
          this.connections = data; // Set fetched data to connections array
        })
        .catch(error => {
            this.errorVisible = true;
            this.tabelError = error;
        });
    },
    async submitPostgressForm() {
    try {
        const response = await fetch("http://127.0.0.1:5000/addPostgresqlConnection", {
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
            }
        
    } catch (error) {
        this.errorVisible = true;
        this.tabelError = error;
    }
},
    async deleteConnection(connection){
        try{
            const response = await fetch("http://127.0.0.1:5000/deleteConnection",{
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"connectionId":connection.connectionId})
            });
            if (!response.ok) {
                this.errorVisible = true;
                this.tabelError = response.status;
            }
            else{
                this.fetchConnections()
            }

        } catch (error){
            this.errorVisible = true;
            this.tabelError = error;
        }
    }
}
}
    
</script>