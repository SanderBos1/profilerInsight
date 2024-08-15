<template>
<div class="row">
    <div class="col-sm-12 col-md-2 order-sm-1 order-md-2 text-sm-center text-center">
        <div class="row">
            <button class="col-md-6 col-sm-6  orange btn btn-secondary" @click="uploadCSV = true" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Here you can upload a file to profile."> Upload</button>
            <button class="col-md-6 col-sm-6 orange btn btn-secondary" @click="deleteCSVDialogue = true" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Here you can Delete one of your uploaded files"> Delete</button>
        </div>
        <h1 align="center mt-3" > File Profiler</h1>
        <select v-model="selectCSVFile" id="selectCSV" class="form-select" data-bs-toggle="tooltip" data-bs-placement="right" title="Choose which file you want to profile.">
            <option disabled selected value="">Choose a File to Profile.</option>
            <option v-for="csvfile in csvFiles" :key="csvfile">
                {{ csvfile }} 
            </option>
        </select> 
        <h2 class="w-100 text-center mt-3">Columns</h2>
        <div class="btn-group-vertical w-100" id="columnButton">
            <button v-for="fileColumn in fileColumns" :key="fileColumn" class="orange btn btn-secondary" @click="getOverview(fileColumn)" data-bs-toggle="tooltip" data-bs-placement="right" title="Click this button to Profile the data in this column">{{ fileColumn }}</button>
        </div>
    </div>
    <div class="col-md-10 order-sm-2 order-md-1">
        <div v-if=columnInfo >
            <baseIngestionOverview
                :columnInfo="columnInfo.overview"
                :example="columnInfo.example"
            ></baseIngestionOverview>
        </div>
    </div>
</div>
   
    <basicDialogue :visible="deleteCSVDialogue"  @update:visible="deleteCSVDialogue = $event" dialogTitle="Delete CSV">
        <template v-slot:dialogueBody>
            <select v-model="toBeDeleteCSV" id="deleteCSV" class="form-control">
                <option disabled selected value="" >Choose a CSV File to Delete.</option>
                <option v-for="csvfile in csvFiles" :key="csvfile">
                    {{ csvfile}} 
                </option>
            </select> 
        </template>
        <template v-slot:dialogueFooter>
            <button class="btn btn-primary" @click="deleteCSV()">Delete</button>
        </template>
    </basicDialogue>
    <basicDialogue :visible="uploadCSV"  @update:visible="uploadCSV = $event" dialogTitle="Upload CSV">
        <template v-slot:dialogueBody>
            <div class="col-md-12 mt-3">
                <form id="csvForm" v-on:submit.prevent="submitCSV" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <div class="mb-3">
                            <label for="CSVProperties" class="form-label">delimiter</label>
                            <select id="CSVProperties" class="form-control" v-model="CSVProperties.csvSeperator" data-bs-toggle="tooltip" title="Choose which value seperates your values and columns in your file.">
                                <option disabled selected value="" >Choose a delimiter , is the default option</option>
                                <option value=",">,</option>
                                <option value=";">;</option>
                                <option value="\t">\t</option>
                            </select>                  
                        </div>
                        <div class="mb-3">
                            <label for="headerRow" class="form-label">headerRow</label>
                            <input type="number" min="0" placeholder="0" id="headerRow" v-model="CSVProperties.headerRow" class="form-control" data-bs-toggle="tooltip" title="Choose which row defines the columns in your file.">
                        </div>
                        <div class="mb-3">
                            <label for="quoteChar" class="form-label">quoteChar</label>
                            <input type="text" id="quoteChar" placeholder='"' v-model="CSVProperties.quoteChar" class="form-control" data-bs-toggle="tooltip" title="Define which characters enclose your values so that the seperator is ignored in your files.">
                        </div>
                        <div class="mb-3">
                            <label for="csvFile" class="form-label">csv File</label>
                            <input type="file" id="csvFile" v-on:change="handleFileUpload" class="form-control"  data-bs-toggle="tooltip" title="Choose which file to upload, current supported extensions are csv and xlsx.">
                        </div>
                            <button class="btn btn-primary" type="submit">Submit</button>
                        </div>
                    </form>
                </div>
        </template>
    </basicDialogue>
    <div class="row">
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

export default {
    name: 'csvProfiler',
    components:{
        baseIngestionOverview,
    },
    data() {
        return {
        toBeDeleteCSV: '',
        selectCSVFile: '',
        deleteCSVDialogue: false,
        uploadCSV: false,
        error: "",
        fileColumns: [],
        csvFiles: [],
        columnInfo: null,
        CSVProperties:{
            csvSeperator: "",
            headerRow: "",
            quoteChar: "",
            csvFile: null
        }
    };
  },
  mounted(){
    this.getCSVFiles();
  },
  watch: {
    selectCSVFile(){
        this.getColumns();
    }
    },
  methods:{
    closeError() {
        this.error = "";
    },
    async deleteCSV() {
        const apiEndpoint = this.$API_ENDPOINTS.DELETE_CSV_FILE(this.toBeDeleteCSV);
        await this.$fetchData(apiEndpoint, 'DELETE')
        .then((data) => {
            if ("Message" in data) {
                this.getCSVFiles();
                this.fileColumns = [],
                this.columnInfo = null;
            }
            else{
                this.error = data["Error"]
            }
        });
    },
    async getCSVFiles() {
        const apiEndpoint = this.$API_ENDPOINTS.GET_CSV_FILES;
        await this.$fetchData(apiEndpoint, 'GET')
            .then((data) => {
                if ("Answer" in data) {
                    this.csvFiles = data["Answer"];
                }
                else{
                    this.error = data["Error"]
                }
        });
    },
    async getColumns() {
        if (!this.selectCSVFile) return;
        const apiEndpoint = this.$API_ENDPOINTS.GET_CSV_COLUMNS(this.selectCSVFile);
        this.csvColumns = await this.$fetchData(apiEndpoint, 'GET')
        .then((data) => {
            if (!("Error" in data)) {
                this.fileColumns = data["Answer"];
                this.columnInfo = null;
            }
            else{
                this.error = data["Error"]
            }
        });
    
    },
    handleFileUpload(event) {
            const file = event.target.files[0]
            this.CSVProperties.csvFile = file;
    },
    async getOverview(csvColumn) {
        const apiEndpoint = this.$API_ENDPOINTS.GET_COLUMN_OVERRVIEW(this.selectCSVFile, csvColumn);
        await this.$fetchData(apiEndpoint, 'GET')
            .then((data) => {
                if (!("Error" in data)) {
                    this.columnInfo=data;
                }
                else{
                    this.error = data["Error"]
                }
            });
    },
    async submitCSV() {
        const formData = new FormData();
        const { csvSeperator, headerRow, quoteChar, csvFile } = this.CSVProperties;

        if (csvSeperator) formData.append('csvSeperator', csvSeperator);
        if (headerRow) formData.append('headerRow', headerRow);
        if (quoteChar) formData.append('quoteChar', quoteChar);
        if (csvFile) formData.append('flatDataSet', csvFile);

        try {
            const response = await fetch(this.$API_ENDPOINTS.UPLOAD_CSV, {
            method: 'POST',
            body: formData
            });

            if (!response.ok) {
                const data = await response.json();
                this.error = data['Error'];
                return;
                }

            await this.getCSVFiles();
            this.uploadCSV = false;
        } catch (error) {
            this.error = error.message;
        }
    }
  }
}
</script>