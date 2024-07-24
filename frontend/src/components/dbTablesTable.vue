<template>
    <div class="row mt-3">
        <div class="offset-md-10">
            <button class="btn btn-secondary" @click="showAddTable = true" >Add Table</button>    
        </div>
    </div>
    <div class="row mt-3">
        <div class="col-md-12">
            <table class="table" id="connectionTable">
                <thead class="thead-dark">
                    <tr>
                        <th scope="col">Table ID</th>
                        <th scope="col">connectionId</th>
                        <th scope="col">schema</th>
                        <th scope="col">table</th>
                    </tr>
                </thead>
                <tbody> 
                    <tr v-for="dbTableConnection in dbTableConnections" :key="dbTableConnection.uniqueTableName">
                        <td>{{ dbTableConnection.uniqueTableName }}</td>
                        <td>{{ dbTableConnection.connectionId }}</td>
                        <td>{{ dbTableConnection.schema }}</td>
                        <td>{{ dbTableConnection.table }}</td>
                        <td><button class="btn" @click="deleteTable(dbTableConnection.uniqueTableName)">Remove</button></td>
                    </tr>      
            </tbody>
            </table>
        </div>
    </div>
    <basicDialogue :visible="showAddTable"  @update:visible="showAddTable = $event" dialogTitle="Postgres Connection">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    <form v-on:submit.prevent="submitPostgressForm" id="addConnectionForm">
                        <div class="mb-3">
                            <label for="connectionId" class="form-label">tableID</label>
                            <input type="text" id="connectionId"  v-model="postgresConnectionForm.uniqueTableName" class="form-control">
                        </div>
                    <div class="mb-3">
                        <label for="host" class="form-label">connectionId</label>
                        <select id="connectionId" v-model="postgresConnectionForm.connectionId" class="form-control">
                            <option v-for="connectionID in connectionIDs" :key="connectionID">
                                {{ connectionID}} 
                            </option>
                        </select>                    
                    </div>
                    <div class="mb-3">
                        <label for="port" class="form-label">schema</label>
                        <input type="text" id="port" v-model="postgresConnectionForm.schema" class="form-control">
                    </div>
                    <div class="mb-3">
                        <label for="username" class="form-label">table</label>
                        <input type="text" id="username" v-model="postgresConnectionForm.table" class="form-control">
                    </div>
                        <button class="btn btn-primary">Submit</button>
                    </form>
                </div>
            </template>
    </basicDialogue>
</template>

<script>
import basicDialogue  from './basicDialogue.vue'

export default {
    name: 'dbTablesTable',
    components:{
        basicDialogue
    },
    data() {
        return {
        showAddTable: false,
        dbTableConnections: [],
        connectionIDs: [],
        postgresConnectionForm:{
            uniqueTableName: "",
            connectionId: "",
            schema: "",
            table: "",
        }
    };
  },
  created() {
    // Fetch data when component is created
    this.fetchConnections();
  },
  mounted() {
    this.getConnectionIDs(); // Fetch connections when the component is mounted
  },
  methods: {
    getConnectionIDs(){
        const apiEndpoint = 'http://127.0.0.1:5000/getConnectionIDs';
        fetch(apiEndpoint)
          .then(response => response.json())
          .then(data => {
            this.connectionIDs = data; 
          })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    },
    changeModals(){
        this.showAddTable = !this.showModal;
    },
    fetchConnections() {
      const apiEndpoint = 'http://127.0.0.1:5000/getTables';
      fetch(apiEndpoint)
        .then(response => response.json())
        .then(data => {
          this.dbTableConnections = data['columnNames']; // Set fetched data to connections array
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
    async submitPostgressForm() {
    try {
        const response = await fetch("http://127.0.0.1:5000/addTable", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(this.postgresConnectionForm)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.fetchConnections();
    } catch (error) {
        console.error("Error adding connection:", error);
    }
},
    async deleteTable(uniqueTableName){
        try{
            const response = await fetch("http://127.0.0.1:5000/deleteTable",{
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({"uniqueTableName":uniqueTableName})
            });
            if(response.ok){
                this.fetchConnections()
            }

        } catch (error){
            console.error("Error deleting connection:", error);
        }
    }
}
}
    
</script>