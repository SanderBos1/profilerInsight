<template>
    <div class="card">
        <div class="card-header">
            <div class="row">
                <div class="col-md-10 col-sm-10">
                    <h3>{{ connection.connection_id }}</h3>
                </div>
                <div class="col-md-2">
                    <button class="btn btn-danger" @click="deleteConnection(connection.connection_id)">X</button>
                </div>
            </div>
        </div>
        <div class="card-body">
            <RouterLink :to="`/connectionOverview/${connection.connection_id}`" >
                <div class="row">
                    <div class="col-md-6 col-sm-6">
                        <img :src="dbDict[connection.db_type]" class="img-fluid" alt="Database Logo">
                    </div>
                    <div class="col-md-6">
                        <div class="row">
                            <div class="col-md-2">
                                <div class="connection-icon__icon">
                                    <font-awesome-icon :icon="['fas', 'server']" />
                                </div> 
                            </div>
                            <div class="col-md-10">
                                <p>{{ connection.server }}</p>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-2">
                                <div class="connection-icon__icon">
                                    <font-awesome-icon :icon="['fas', 'database']" />
                                </div>
                            </div>
                            <div class="col-md-10">
                                <p>{{ connection.database }}</p>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-2">
                                <div class="connection-icon__icon">
                                    <font-awesome-icon :icon="['fas', 'user']" />
                                </div>
                            </div>
                            <div class="col-md-10">
                                <p>{{ connection.username }}</p>
                            </div>
                        </div>
                    </div>  
                </div>
            </RouterLink>
        </div>
    </div>
</template>


<script>


export default {
    name: "connectionIcon",
    props: {
        connection: {
            type: Object,
            required: true
        }
    },
    emits: ['fetchConnections'],

    data() {
        return {
            dbDict : {
                'postgres': require('../assets/Images/postgresLogo.jpg'),
                'azuresql':require('../assets/Images/azureSQLDatabaseIcon.svg')

            },
            showDetails: false
        }
    },
    methods:{
        async deleteConnection(connection_id) {
        const apiEndpoint = this.$API_ENDPOINTS.DELETE_CONNECTION(connection_id);
        await this.$fetchData(apiEndpoint, 'DELETE')
            .then((data) => {
                if ("Error" in data) {
                    this.error = data["Error"]
                }
                else{
                    this.$emit('fetchConnections');
                }
        });

    },
    }
}

</script>