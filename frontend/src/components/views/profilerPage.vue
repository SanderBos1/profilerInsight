<template>

    <!-- Main container row for the component -->
    <div class="row">
        <h2 align="center">Database Profiler</h2>

    <!-- Table selector and column display  -->
        <div class="col-sm-12 col-md-2 order-sm-1 order-md-2 text-sm-center text-center">
            <label for="exampleDataList" class="form-label">Choose Table to Profile</label>
            <input   v-model="selectedTable" class="form-control" list="datalistOptions" id="exampleDataList" placeholder="Type to search..."/>
            <datalist id="datalistOptions">
                <option v-for="table in tables" :key="table.table_id" :value="table.table_id">
                    {{ table.connection_id }}: {{ table.db_name }} - {{ table.schemaName }}.{{ table.tableName }}
                </option>
            </datalist>
            <h2 class="w-100 text-center mt-3">Columns</h2>
                <div class="btn-group-vertical w-100" id="columnButton">
                    <button v-for="tableColumn in tableColumns" :key="tableColumn" class="orange btn btn-secondary" @click="getOverview(tableColumn)" data-bs-toggle="tooltip" data-bs-placement="left" title="Click this button to Profile the data in this column">{{ tableColumn }}</button>
                </div>
        </div>


    <!-- profiler Overview -->
        <div class="col-sm-12 col-md-10 order-sm-2 order-md-1 text-sm-center text-center">
            <div v-if='encourageIngestion' class="alert alert-warning" role="alert">
                {{ encourageIngestion }}
            </div>
            <div v-if='selectedColumn'>
                <div class="row">
                    <div class="col-md-9 mt-3">
                        <h3 align="center">{{ this.selectedColumn }}</h3>
                    </div>
                <div class="col-md-3 mt-3">
                    <button class="btn btn-primary grey" @click="ingestColumnData(this.selectedTable, this.selectedColumn)" data-bs-toggle="tooltip" title="Calculates data corresponding to the profiler and loads it to the database">Ingest</button>
                </div>
            </div>
            <div v-if=profilerOverview >
                <baseIngestionOverview
                    :columnInfo="profilerOverview.overview"
                    :example="profilerOverview.example"
                ></baseIngestionOverview>
        </div>
        </div>
    </div>

    <!-- error Display -->
    <errorDialogue :error="error"  @closeError="closeError" dialogTitle="file Error">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    {{error }}
                </div>
            </template>
    </errorDialogue>


    </div>
</template>

<script>
import baseIngestionOverview from '../profilerOverview.vue';

export default{
    name: "profilerPage",
    components:{
        baseIngestionOverview,
    },
    data(){
        return{
            tables: [],
            selectedTable: '',
            error: "",
            tableColumns: [],
            selectedColumn: '',
            profilerOverview: {},
            encourageIngestion: ""
        }
    },
    mounted(){
        this.getTables();
    },
    watch:{
        selectedTable(){
            this.getColumns();
        }
        
    },
    methods:{

    closeError() {
        this.error = "";
    },
    async getColumns(){
        this.profilerOverview = "";
        this.encourageIngestion = "";
        const url = this.$API_ENDPOINTS.get_table_columns(this.selectedTable);
        const data = await this.$fetchData(url, "get");
        if(data){
            this.tableColumns = data;
        }

    },
    async getTables(){
        const url = this.$API_ENDPOINTS.GET_CONNECTED_TABLES
        const method = "GET";
        await this.$fetchData(url, method)
            .then((data) => {
                if ("Answer" in data) {
                    this.tables = data['Answer'];
                }
                else{
                    this.error = data["Error"]
                }
        });

    },
    async getOverview(column){
        this.profilerOverview = "";
        this.selectedColumn = column;
        const url = this.$API_ENDPOINTS.get_overview_data(this.selectedTable, column);
        await this.$fetchData(url, "GET")
            .then((data) => {
                if (!("Message" in data)) {
                    this.profilerOverview = data;
                    this.encourageIngestion = ""
                }
                else{
                    this.encourageIngestion = "Please ingest your data first"
                }
        });
    },
    async ingestColumnData(table, column){
        const url = this.$API_ENDPOINTS.get_ingestion_data(column, table);

        await this.$fetchData(url, "GET")
            .then((data) => {
                if ("Message" in data){
                    this.getOverview(column);
                }
                else{
                    this.error = data["Message"]
                }
            });
        }
    }
}
</script>