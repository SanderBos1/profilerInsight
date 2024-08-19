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
            <div v-if='encourageIngestion' class="alert alert-warning" role="alert">
                {{ encourageIngestion }}
            </div>
            <div v-if='selectedColumn'>
                <div class="row">
                <div class="col-md-3 mt-3">
                    <button class="btn btn-primary grey" @click="ingestColumnData(this.table_id, this.selectedColumn)" data-bs-toggle="tooltip" title="Calculates data corresponding to the profiler and loads it to the database">Ingest</button>
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
    },
    data(){
        return{
            columns: [],
            error: "",
            encourageIngestion: "",
            profilerOverview: {},
            selectedColumn: "",
        }
    },
    methods:{
        closeError() {
            this.error = "";
        },
        async getColumns(){
            const url = this.$API_ENDPOINTS.get_table_columns(this.table_id);
            const data = await this.$fetchData(url, "get");
            if("Error" in data){
                this.error = data["Error"];
            }
            else{
                this.columns = data["Answer"];
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
    async ingestColumnData(table, column){
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
        }
    }
}
</script>