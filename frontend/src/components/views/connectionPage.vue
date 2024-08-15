<template>
    <div class="row mt-3">
        <addConncetion  @loadConnections="fetchConnections" @ingestTables="ingestTables"></addConncetion>
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
                        <td>*****</td> 
                        <td>{{ connection.database }}</td>
                        <td>{{ connection.db_type}}</td>
                        <td><button class="btn btn-primary grey" @click="deleteConnection(connection.connection_id)" data-bs-toggle="tooltip" title="Removes the connection, and everything connected to it.">Remove</button></td>
                    </tr>      
            </tbody>
            </table>
        </div>
    </div>
    <errorDialogue :error="error"  @closeError="closeError" dialogTitle="connection Error">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    {{error }}
                </div>
            </template>
    </errorDialogue>

</template>

<script>
import addConncetion from '../addConnection.vue';


export default {
    name: 'tablePage',
    components:{
        addConncetion,
    },
    data() {
        return {
        errorVisible: false,
        error: "",
        connections: [],
    };
  },
  created() {
    this.fetchConnections();
  },
  methods: {
    closeError() {
        this.error = "";
    },

    async fetchConnections() {
      const apiEndpoint = this.$API_ENDPOINTS.GET_CONNECTIONS;
      await this.$fetchData(apiEndpoint, 'GET')
        .then((data) => {
            if ("Answer" in data) {
                this.connections = data["Answer"];
            }
            else{
                this.error = data["Error"]
            }
        });
    },

    async deleteConnection(connection_id) {
        const apiEndpoint = this.$API_ENDPOINTS.DELETE_CONNECTION(connection_id);
        await this.$fetchData(apiEndpoint, 'DELETE')
            .then((data) => {
                if ("Error" in data) {
                    this.error = data["Error"]
                }
                else{
                    this.fetchConnections();
                }
        });

    },
    async ingestTables(){
        const apiEndpoint = this.$API_ENDPOINTS.ingest_connection_tables;
        await this.$fetchData(apiEndpoint, 'GET')
            .then((data) => {
                if ("Error" in data) {
                    this.error = data["Error"]
                }

        });
    },
}};
    
</script>