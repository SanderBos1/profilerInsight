<template>
    <div class="row">
        <div class="col-sm-12 col-md-3">
            <h1 align="center"> CSV Profiler</h1>
        </div>
        <div class="col-sm-12 offset-md-6 col-md-3 text-sm-center text-center">
            <button class="orange  btn btn-secondary" @click="uploadCSV = true" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Here you can upload a CSV file to profile."> Upload</button>
            <button  class="orange  btn btn-secondary ms-3" @click="deleteCSVDialogue = true" data-bs-toggle="tooltip" data-bs-placement="bottom" title="Here you can Delete one of your uploaded CSV files"> Delete</button>
        </div>
    </div>
    <div class="row">
        <div class="col-sm-12 col-md-3">
            <select v-model="selectCSVFile" id="selectCSV" class="form-select" data-bs-toggle="tooltip" data-bs-placement="right" title="Choose which CSV file you want to profile.">
                <option disabled selected value="" >Choose a CSV File to Profile.</option>
                <option v-for="csvfile in csvFiles" :key="csvfile">
                    {{ csvfile}} 
                </option>
            </select> 
            <h2 class="w-100 text-center">Columns</h2>
            <div class="btn-group-vertical w-100" id="columnButton">
                <button v-for="csvColumn in csvColumns" :key="csvColumn" class="orange btn btn-secondary" @click="getOverview(csvColumn)" data-bs-toggle="tooltip" data-bs-placement="right" title="Click this button to Profile the data in this column">{{ csvColumn }}</button>
            </div>
        </div>
        <div class="col-md-9">
            <baseIngestionOverview :columnInfo=columnInfo>
            </baseIngestionOverview>
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
                            <label for="CSVProperties" class="form-label">Seperator</label>
                            <select id="CSVProperties" class="form-control" v-model="CSVProperties.csvSeperator" data-bs-toggle="tooltip" title="Choose which value seperates your values and columns in your CSV.">
                                <option disabled selected value="" >Choose a CSV Seperator , is the default option</option>
                                <option value=",">,</option>
                                <option value=";">;</option>
                                <option value="\t">\t</option>
                            </select>                  
                        </div>
                        <div class="mb-3">
                            <label for="headerRow" class="form-label">headerRow</label>
                            <input type="number" min="0" placeholder="0" id="headerRow" v-model="CSVProperties.headerRow" class="form-control" data-bs-toggle="tooltip" title="Choose which row defines the columns in your CSV file.">
                        </div>
                        <div class="mb-3">
                            <label for="quoteChar" class="form-label">quoteChar</label>
                            <input type="text" id="quoteChar" placeholder='"' v-model="CSVProperties.quoteChar" class="form-control" data-bs-toggle="tooltip" title="Define which characters enclose your values so that the seperator is ignored in your CSV Files.">
                        </div>
                        <div class="mb-3">
                            <label for="csvFile" class="form-label">csv File</label>
                            <input type="file" id="csvFile" v-on:change="handleFileUpload" class="form-control" accept=".csv" data-bs-toggle="tooltip" title="Choose which csv file to upload.">
                        </div>
                            <button class="btn btn-primary" type="submit">Submit</button>
                        </div>
                    </form>
                </div>
        </template>
    </basicDialogue>
    <div class="row">
        <basicDialogue :visible="errorVisible"  @update:visible="errorVisible = $event" dialogTitle="CSV Profiler Error">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    {{csvUploadError }}
                </div>
            </template>
        </basicDialogue>
    </div>
</template>

<script>
import basicDialogue  from '../baseDialogue.vue'
import baseIngestionOverview from '../baseIngestionOverview.vue';

const API_ENDPOINTS = {
  GET_CSV_FILES: 'http://127.0.0.1:5000/getCSVFiles',
  DELETE_CSV_FILE: file => `http://127.0.0.1:5000/deleteCSVFile/${file}`,
  GET_CSV_COLUMNS: file => `http://127.0.0.1:5000/getCSVColumns/${file}`,
  GET_COLUMN_OVERRVIEW: (file, column) => `http://127.0.0.1:5000/getColumnOverview/${file}/${column}`,
  UPLOAD_CSV: 'http://127.0.0.1:5000/uploadCSV'
};

export default {
    name: 'csvProfiler',
    components:{
        basicDialogue,
        baseIngestionOverview
    },
    data() {
        return {
        toBeDeleteCSV: '',
        selectCSVFile: '',
        deleteCSVDialogue: false,
        uploadCSV: false,
        errorVisible: false,
        csvUploadError: "",
        csvColumns: [],
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
        this.csvUploadError = message;
    },
    async deleteCSV() {
        const apiEndpoint = API_ENDPOINTS.DELETE_CSV_FILE(this.toBeDeleteCSV);
        await this.fetchData(apiEndpoint, 'DELETE');
        this.getCSVFiles();
        this.csvColumns = [],
        this.columnInfo = null;

    },
    async getCSVFiles() {
        const apiEndpoint = API_ENDPOINTS.GET_CSV_FILES;
        this.csvFiles = await this.fetchData(apiEndpoint, 'GET');
    },
    async getColumns() {
        if (!this.selectCSVFile) return;
        const apiEndpoint = API_ENDPOINTS.GET_CSV_COLUMNS(this.selectCSVFile);
        this.csvColumns = await this.fetchData(apiEndpoint, 'GET');
        this.columnInfo = null;
    
    },
    handleFileUpload(event) {
            const file = event.target.files[0]
            this.CSVProperties.csvFile = file;
        },
    async getOverview(csvColumn) {
        const apiEndpoint = API_ENDPOINTS.GET_COLUMN_OVERRVIEW(this.selectCSVFile, csvColumn);
        this.columnInfo = await this.fetchData(apiEndpoint, 'GET');
    },
    async submitCSV() {
        const formData = new FormData();
        const { csvSeperator, headerRow, quoteChar, csvFile } = this.CSVProperties;

        if (csvSeperator) formData.append('csvSeperator', csvSeperator);
        if (headerRow) formData.append('headerRow', headerRow);
        if (quoteChar) formData.append('quoteChar', quoteChar);
        if (csvFile) formData.append('csvFile', csvFile);

        try {
            const response = await fetch(API_ENDPOINTS.UPLOAD_CSV, {
            method: 'POST',
            body: formData
            });

            if (!response.ok) {
                this.handleError(response.statusText);
                return;
                }

            await this.getCSVFiles();
            this.uploadCSV = false;
        } catch (error) {
            this.handleError(error.message);
  }
}
  }
}
</script>