<template>
    <div class="row">
        <div class="col-md-3 mb-3">
            <h2 class="text-center">Table</h2>
            <select v-model="selectedTable" id="uniqueTableName" class="form-control">
                <option v-for="uniqueTableName in uniqueTableNames" :key="uniqueTableName">
                    {{ uniqueTableName}} 
                </option>
            </select> 
            <h2 class="w-100 text-center">Columns</h2>
            <div class="btn-group-vertical w-100" id="columnButton">
                <button v-for="column in columns" :key="column" class="btn btn-secondary" @click="getOverview(column)">{{ column }}</button>
            </div>
        </div>
        <basicDialogue :visible="errorVisible"  @update:visible="errorVisible = $event" dialogTitle="csv Upload Error">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    {{ profilerError }}
                </div>
            </template>
    </basicDialogue>
        <div class="col-md-9 mt-3" v-if="overview">
            <div class="row">
                <div class="col-md-9">
                <h5>{{ column }}</h5>
                </div>
            <div class="col-md-3">
                <button class="btn btn-primary w-100" @click="ingestColumn()">Ingest</button>
            </div>
        </div>
            <div class="row mt-2">
            <div class="col-md-6">
                <p><strong>Column Type:</strong> {{ overview.columnType }}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Distinct Values:</strong> {{ overview.distinctValues }}</p>
            </div>
            <div class="col-md-6">
                <p><strong>NaN Values:</strong> {{ overview.nanValues }}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Row Count:</strong> {{ overview.rowCount }}</p>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import basicDialogue  from './baseDialogue.vue'

export default{
    components:{
        basicDialogue
    },
    name: 'profilerPage',
    data(){
        return{
            profilerError: "",
            errorVisible: false,
            uniqueTableNames: [],
            columns: [],
            selectedTable: null,
            overview: null,
            column: null
            }
        },

    mounted(){
        this.getConnectionIDs();
    },
    watch: {
        selectedTable(){
            this.getColumns();
        }
    },
    methods:{
        getConnectionIDs(){
            const apiEndpoint = 'http://127.0.0.1:5000/getUniqueTableNames';
            fetch(apiEndpoint)
            .then(response => response.json())
            .then(data => {
                this.uniqueTableNames = data; 
            })
            .catch(error => {
                this.errorVisible = true;
                this.profilerError = error;
            });
        },
        getColumns(){
            const apiEndpoint = 'http://127.0.0.1:5000/getColumns/' + this.selectedTable;
            fetch(apiEndpoint)
            .then(response => response.json())
            .then(data => {
                this.columns = data['columnNames']; 
            })
            .catch(error => {
                this.errorVisible = true;
                this.profilerError = error;
            });
        },
        getOverview(column){
            const apiEndpoint = 'http://127.0.0.1:5000/getOverview/' + this.selectedTable  + "/" + column;
            fetch(apiEndpoint)
            .then(response => {
                if (!response.ok) { 
                    const error = new Error('Error fetching data');
                    this.errorVisible = true;
                    throw error;
                }
                return response.json();
            })
            .then(data => {
                this.overview = data
                this.column = column
            })
            .catch(error => {
                this.errorVisible = true;
                this.profilerError = error;
            });
    },
    ingestColumn(){
            const apiEndpoint = 'http://127.0.0.1:5000/ingest/' + this.selectedTable  + "/" + this.column;
            fetch(apiEndpoint)
            .then(response => {
                if (!response.ok) { 
                    const error = new Error('Error fetching data, so no ingestion was done.');
                    this.errorVisible = true;
                    throw error;
                }
                return response.json();
            })
            .then(data => {
                this.overview = data
            })
            .catch(error => {
                this.errorVisible = true;
                this.profilerError = error;
            });
        }
    }
}
</script>