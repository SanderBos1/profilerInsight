<template>

    <!-- Main container row for the component -->
    <div class="row">

    <!-- Table selector and column display  -->
        <div class="col-sm-12 col-md-2 order-sm-1 order-md-2 text-sm-center text-center">
            <h2 class="w-100 text-center mt-3">Columns</h2>
                <div class="btn-group-vertical w-100" id="columnButton">
                    <button v-for="column in columns" :key="column" class="orange btn btn-secondary" @click="getOverview(column)" data-bs-toggle="tooltip" data-bs-placement="left" title="Click this button to Profile the data in this column">{{ column }}</button>
                </div>
        </div>


    <!-- profiler Overview -->
        <div class="col-sm-12 col-md-10 order-sm-2 order-md-1 text-sm-center text-center">
            <div class="row">
                <h3> Data Profiler of {{ table_info.schema_name }}.{{ table_info.table_name }}</h3>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="btn-group w-100" id="columnButton">                    
                        <button class="btn btn-primary grey" @click="returnTableOverview">Return</button>
                        <button class="btn btn-primary grey" @click="changeView">Quality</button>
                        <button v-if='selectedColumn'  class="btn btn-primary grey" @click="ingestColumnData(this.selectedColumn)" data-bs-toggle="tooltip" title="Calculates data corresponding to the profiler and loads it to the database">
                        Ingest</button>
                    </div>
                </div>  
            </div>
            <div v-if='encourageIngestion' class="alert alert-warning" role="alert">
                {{ encourageIngestion }}
            </div>
            <div v-if=profilerOverview >
                <baseIngestionOverview
                    :columnInfo="profilerOverview.overview"
                    :example="profilerOverview.example"
                ></baseIngestionOverview>
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

    name: "DbTableView",
    components:{
        baseIngestionOverview,
    },
    props:{
        tableID: String,
    },
    computed: {
        table_id() {
        return this.$route.params.table_id;
        }
    },
    mounted(){
        this.getColumns();
        this.setTableInfo();
    },
    data(){
        return{
            columns: [],
            error: "",
            encourageIngestion: "",
            profilerOverview: {},
            selectedColumn: "",
            table_info: {}
        }
    },
    methods:{
        changeView(){
            this.$router.push({path: `/tableQualityView/${this.table_id}`})
        },
        closeError() {
            this.error = "";
        },
        returnTableOverview(){
           this.$router.push({path: `/connectionOverview/${this.table_info.connection_id}`});

        },
        async getColumns(){
            const url = this.$API_ENDPOINTS.get_table_columns(this.table_id);
            const data = await this.$fetchData(url, "get");
            if("Error" in data){
                this.error = data["Error"];
            }
            else{
                this.columns = data["Answer"];
                this.selectedColumn = this.columns[0];
            }
        },
        async getOverview(column){
            this.profilerOverview = "";
            this.selectedColumn = column;
            const url = this.$API_ENDPOINTS.get_overview_data(this.table_id, column);
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
        async ingestColumnData(column){
            const url = this.$API_ENDPOINTS.get_ingestion_data(column, this.table_id);

            await this.$fetchData(url, "GET")
                .then((data) => {
                    if ("Message" in data){
                        this.getOverview(column);
                    }
                    else{
                        this.error = data["Message"]
                    }
                });
            },
        async setTableInfo(){
        
            const url = this.$API_ENDPOINTS.GET_TABLE_INFO(this.table_id);

            await this.$fetchData(url, "GET")
                .then((data) => {
                    if ("Answer" in data){
                        this.table_info = data["Answer"];
                    }
                    else{
                        this.error = data["Message"]
                    }
                });

            }
        }   
    }
</script>