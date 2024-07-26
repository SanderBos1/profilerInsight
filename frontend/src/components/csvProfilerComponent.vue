<template>
    <div class="row">
        <div class="col-md-3">
            <h1> CSV Profiler</h1>
        </div>
        <div class="offset-md-4 col-md-2">
            <button @click="uploadCSV = true"> Upload csv </button>
        </div>
        <div class="col-md-2">
            <button> Delete CSV </button>
        </div>
    </div>
        <div class="row">
            <div class="col-md-3">
                <select v-model="selectCSVFile" id="uniqueTableName" class="form-control">
                    <option v-for="csvfile in csvFiles" :key="csvfile">
                        {{ csvfile}} 
                    </option>
                </select> 
                <h2 class="w-100 text-center">Columns</h2>
                <div class="btn-group-vertical w-100" id="columnButton">
                    <button v-for="csvColumn in csvColumns" :key="csvColumn" class="btn btn-secondary" @click="getOverview(csvColumn)">{{ csvColumn }}</button>
                </div>
            </div>
            <div class="col-md-9">
                <baseIngestionOverview :columnInfo=columnInfo>
                </baseIngestionOverview>
            </div>
        </div>
            <basicDialogue :visible="uploadCSV"  @update:visible="uploadCSV = $event" dialogTitle="Upload CSV">
                <template v-slot:dialogueBody>
                    <div class="col-md-3 mt-3">
                        <form id="csvForm" v-on:submit.prevent="submitCSV" method="post" enctype="multipart/form-data">
                            <div class="form-group">
                                <div class="mb-3">
                                    <label for="csvSeperator" class="form-label">Seperator</label>
                                    <select id="csvSeperator" class="form-control" v-model="csvProfilerForm.csvSeperator">
                                        <option value=','>,</option>
                                        <option value=';'>;</option>
                                        <option value='\t'>\t</option>
                                    </select>                  
                                </div>
                                <div class="mb-3">
                                    <label for="headerRow" class="form-label">headerRow</label>
                                    <input type="number" min="0" value="0" id="headerRow" v-model="csvProfilerForm.headerRow" class="form-control">
                                </div>
                                <div class="mb-3">
                                    <label for="quoteChar" class="form-label">quoteChar</label>
                                    <input type="text" id="quoteChar"  v-model="csvProfilerForm.quoteChar" class="form-control">
                                </div>
                                <div class="mb-3">
                                    <label for="csvFile" class="form-label">csv File</label>
                                    <input type="file" id="csvFile" v-on:change="handleFileUpload" class="form-control" accept=".csv">
                                </div>
                                <button class="btn btn-primary" type="submit">Submit</button>
                            </div>
                        </form>
                    </div>
                </template>
            </basicDialogue>
<div class="row">
    <basicDialogue :visible="errorVisible"  @update:visible="errorVisible = $event" dialogTitle="csv Upload Error">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    {{csvUploadError }}
                </div>
            </template>
    </basicDialogue>
</div>


</template>

<script>
import basicDialogue  from './baseDialogue.vue'
import baseIngestionOverview from './baseIngestionOverview.vue';

export default {
    name: 'csvProfilerComponent',
    components:{
        basicDialogue,
        baseIngestionOverview
    },
    data() {
        return {
        selectCSVFile: null,
        uploadCSV: false,
        errorVisible: false,
        csvUploadError: "",
        csvColumns: [],
        csvFiles: [],
        columnInfo: null,
        csvProfilerForm:{
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
    getCSVFiles(){
        const apiEndpoint = 'http://127.0.0.1:5000/getCSVFiles';
        fetch(apiEndpoint)
        .then(response => response.json())
        .then(data => {
            this.csvFiles = data; 
        })
        .catch(error => {
                this.errorVisible = true;
                this.csvUploadError = error;
            });
    },
    getColumns(){
        const apiEndpoint = 'http://127.0.0.1:5000/getCSVColumns/' + this.selectCSVFile;
        fetch(apiEndpoint)
        .then(response => response.json())
        .then(data => {
            this.csvColumns = data; 
        })
        .catch(error => {
                this.errorVisible = true;
                this.csvUploadError = error;
            });
        
    },
    handleFileUpload(event) {
            const file = event.target.files[0]
            this.csvProfilerForm.csvFile = file;
        },
    getOverview(csvColumn){
        const apiEndpoint = 'http://127.0.0.1:5000/getColumnOverview/' + this.selectCSVFile + "/" + csvColumn;
        fetch(apiEndpoint)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            this.columnInfo = data; 
        })
        .catch(error => {
                this.errorVisible = true;
                this.csvUploadError = error;
            });
    },
    async submitCSV(){
        const formData = new FormData();
        if (this.csvProfilerForm.csvSeperator != '') {
            formData.append('csvSeperator', this.csvProfilerForm.csvSeperator);
        }
        if (this.csvProfilerForm.headerRow != '') {
            formData.append('headerRow', this.csvProfilerForm.headerRow);
        }
        if (this.csvProfilerForm.quoteChar != '') {
            formData.append('quoteChar', this.csvProfilerForm.quoteChar);
        }
            formData.append('csvFile', this.csvProfilerForm.csvFile);
        try {
            const response = await fetch("http://127.0.0.1:5000/uploadCSV", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            this.columnsInfo = [];
            this.errorVisible = true;
            this.csvUploadError = response.statusText;
            
        }
        else{
            this.getCSVFiles();
            this.uploadCSV = false;

        }
        } 
        catch (error) {
            this.errorVisible = true;
            this.csvUploadError = error;
        }    
    }
  }
}
</script>