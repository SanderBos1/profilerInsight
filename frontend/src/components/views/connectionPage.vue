<template>
    <div class="row mt-3">
        <addConncetion  @loadConnections="fetchConnections"></addConncetion>
    </div>
    <div class="row mt-3">
        <div v-for="connection in connections" :key="connection.connection_id" class="col-md-4 col-sm-6">
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
  
    }
};
    
</script>