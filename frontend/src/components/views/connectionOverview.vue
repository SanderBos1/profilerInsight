<template>
    <div class="row">
        <h2 align="center"> Tables of {{ this.connection_id}}</h2>
    </div>
    <div class="row">
        <input type="text" class="col-md-9" v-model="searchTables" placeholder="Search tables..." />
        <div class="col-md-3">
            <div class="row">
                <button class="col-12 col-md-5 btn btn-secondary grey mt-2 " @click="ingestTables" data-bs-toggle="tooltip" data-bs-placement="left" title="Loads all tables that are connected to this connection and adds them to the database">Load Tables</button>
                <button class="col-12 offset-md-2 col-md-5 btn btn-secondary grey mt-2" @click="previousPage">Return</button>
            </div>
        </div>
    </div>

    <div class="row">
        <div v-if="tables" class="row mt-5">
            <div v-for="table in filteredTables" :key="table.table_id">
                <div class="col-md-4 col-sm-6 col-12">
                    <div class="card">
                        <RouterLink :to="`/DbTableView/${table.table_id}`" >
                            <div class="card-header">
                                <div class="row">
                                    <div class="col-md-2">
                                        <div class="connection-icon__icon">
                                            <font-awesome-icon :icon="['fas', 'table']" />
                                        </div>
                                    </div>
                                    <div class="col-md-10">
                                        <p> {{ table.table_name }}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="card-body">
                                <p> <b>Schema:</b> {{table.schema_name}}</p>
                                <p> <b>Quality:</b> {{table.data_quality}} %</p>

                            </div>
                        </RouterLink>
                    </div>
                </div>
            </div>
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

export default {
    name: "connectionOverview",

    computed: {
        filteredTables() {
            const searchQuery = this.searchTables.toLowerCase();
            return this.tables.filter(table => {
                const table_name = (table.table_name || '').toLowerCase();
                const schema_name = (table.schema_name || '').toLowerCase();

                return (
                    table_name.includes(searchQuery) ||
                    schema_name.includes(searchQuery)
            ) 
            });
        },
        connection_id() {
            return this.$route.params.connection_id;
        }
    },
    mounted(){
        this.loadTables();
    },
    data() {
        return {
            tables: [],
            error: "",
            searchTables: "",
        }
    },
    methods: {
        closeError() {
        this.error = "";
        },
        async ingestTables(){
        const apiEndpoint = this.$API_ENDPOINTS.ingest_connection_tables(this.connection_id);
        await this.$fetchData(apiEndpoint, 'GET')
            .then((data) => {
                if ("Error" in data) {
                    this.error = data["Error"]
                }
                else{
                    this.loadTables();
                }

        });
    },
    async loadTables(){
        const apiEndpoint = this.$API_ENDPOINTS.LOAD_TABLES(this.connection_id);
        this.tables = [];
        await this.$fetchData(apiEndpoint, 'GET')
            .then((data) => {
                if ("Error" in data) {
                    this.error = data["Error"]
                }
                else{
                    this.tables = data["Answer"];
                }

        });
    },
    previousPage(){

        this.$router.push('/connectionPage');
        }
    },

}
    

</script>