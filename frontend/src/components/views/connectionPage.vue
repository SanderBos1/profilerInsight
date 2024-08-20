<template>
    <h3 alling="center">Connections</h3>
    <div class="row mt-3">
        <input type="text" class="col-md-9 mt-2" v-model="searchConnection" placeholder="Search connections..." />
        <addConncetion @loadConnections="fetchConnections"></addConncetion>
    </div>
    <div class="row mt-3">
        <div v-for="connection in filteredConnections" :key="connection.connection_id" class="col-md-4 col-sm-6 col-12  mt-3">
            <connectionIcon :connection="connection" @fetchConnections="fetchConnections"></connectionIcon>
        </div>
        <errorDialogue :error="error"  @closeError="closeError" dialogTitle="connection Error">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    {{error }}
                </div>
            </template>
        </errorDialogue>
    </div>
</template>

<script>
import addConncetion from '../addConnection.vue';
import connectionIcon from '../connectionIcon.vue';

export default {
    name: 'tablePage',
    components:{
        addConncetion,
        connectionIcon
    },
    data() {
        return {
        error: "",
        connections: [],
        searchConnection: "",
    };
  },
  created() {
    this.fetchConnections();
  },
  computed: {
    filteredConnections() {
        const searchQuery = this.searchConnection.toLowerCase();
        return this.connections.filter(connection => {
            return (
                connection.connection_id.toLowerCase().includes(searchQuery) ||
                connection.server.toLowerCase().includes(searchQuery) ||
                connection.database.toLowerCase().includes(searchQuery) ||
                connection.username.toLowerCase().includes(searchQuery) 

        ) 
        });
  } ,
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
  
    }
};
    
</script>