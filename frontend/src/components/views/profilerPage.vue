<template>

    <!-- Main container row for the component -->
    <div class="row">
        <h2 align="center">Database Profiler</h2>

    <!-- Table selector and column display  -->
        <div class="col-sm-12 col-md-2 order-sm-1 order-md-2 text-sm-center text-center">
            <label for="exampleDataList" class="form-label">Choose Table to Profile</label>
            <input   v-model="selectedTable" class="form-control" list="datalistOptions" id="exampleDataList" placeholder="Type to search..."/>
            <datalist id="datalistOptions">
                <option v-for="(table, index) in tables" :key="index" :value="table.table_id">{{ table.connection }}{{ table.schemaName }} {{table.tableName}}</option>
            </datalist>
            <h2 class="w-100 text-center mt-3">Columns</h2>
                <div class="btn-group-vertical w-100" id="columnButton">
                    <button v-for="tableColumn in tableColumns" :key="tableColumn" class="orange btn btn-secondary" @click="getOverview(tableColumn)" data-bs-toggle="tooltip" data-bs-placement="left" title="Click this button to Profile the data in this column">{{ tableColumn }}</button>
                </div>
        </div>


    <!-- profiler Overview -->

        <div class="col-sm-12 col-md-10 order-sm-2 order-md-1 text-sm-center text-center">
            <div v-if='selectedColumn'>
                <div class="row">
                    <div class="col-md-9 mt-3">
                        <h3 align="center">{{ this.selectedColumn[0] }}</h3>
                    </div>
                <div class="col-md-3 mt-3">
                    <button class="btn btn-primary grey" @click="ingestColumnData(this.selectedTable, this.selectedColumn)" data-bs-toggle="tooltip" title="Calculates data corresponding to the profiler and loads it to the database">Ingest</button>
                </div>
                <div v-if="profilerOverview">
                    <dbProfilerOverview :profilerOverview="profilerOverview"></dbProfilerOverview>
                </div>
            </div>
            <div v-if="encourageIngestion">
                {{encourageIngestion}}
            </div>
        </div>
    </div>

    <!-- error Display -->

        <basicDialogue :visible="errorVisible"  @update:visible="errorVisible = $event" dialogTitle="FlatFile Profiler Error">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    {{tablesLoadError }}
                </div>
            </template>
        </basicDialogue>


    </div>
</template>

<script>
import basicDialogue  from '../baseDialogue.vue';
import dbProfilerOverview from '../dbProfilerOverview.vue';

const API_ENDPOINTS = {
    GET_CONNECTED_TABLES: 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + '/api/get_connected_tables',
    get_table_columns: table_id => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/get_columns/${table_id}`,
    get_ingestion_data: (column, table_id) => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/ingest/${table_id}/${column}`,
    get_overview_data: (table, column) => 'http://' + process.env.VUE_APP_FLASK_HOST + ':' + process.env.VUE_APP_FLASK_PORT + `/api/profile_column/${table}/${column}`
};

export default{
    name: "profilerPage",
    components:{
        basicDialogue,
        dbProfilerOverview
    },
    data(){
        return{
            tables: [],
            selectedTable: '',
            errorVisible: false,
            tablesLoadError: "",
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
        this.tablesLoadError = message;
    },
    async getColumns(){
        this.profilerOverview = "";
        this.encourageIngestion = "";
        const url = API_ENDPOINTS.get_table_columns(this.selectedTable);
        const method = "GET";
        const data = await this.fetchData(url, method);
        if(data){
            this.tableColumns = data;
        }

    },
    async getTables(){
        const url = API_ENDPOINTS.GET_CONNECTED_TABLES
        const method = "GET";
        const data = await this.fetchData(url, method);
        if(data){
            this.tables = data;
        }

    },
    async getOverview(column){
        this.profilerOverview = "";
        this.selectedColumn = column;
        const url = API_ENDPOINTS.get_overview_data(this.selectedTable, column);
        const method = "GET";
        const data = await this.fetchData(url, method);
        if(data){
            if(data != "No Dict Found"){
                this.profilerOverview = data;
                this.encourageIngestion = ""
            }
            else{
                this.encourageIngestion = "Please Ingest Data to view Overview"
            }
        }
    },
    async ingestColumnData(table, column){
        const url = API_ENDPOINTS.get_ingestion_data(column, table);
        const method = "GET";
        const data = await this.fetchData(url, method);
        if(data){
            this.getOverview(column);
        }    
    },
}}
</script>