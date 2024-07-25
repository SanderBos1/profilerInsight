<template>
    <div class="row">
        <div class="col-md-3 mt-3">
            <form id="csvForm" v-on:submit.prevent="submitCSV" method="post" enctype="multipart/form-data">
                <div class="form-group">
                    <div class="mb-3">
                        <label for="csvSeperator" class="form-label">csvSeperator</label>
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
    </div>
<div class="row">
    <basicDialogue :visible="errorVisible"  @update:visible="errorVisible = $event" dialogTitle="csv Upload Error">
            <template v-slot:dialogueBody>
                <div class="mb-3">
                    {{csvUploadError }}
                </div>
            </template>
    </basicDialogue>
  <div v-for="columnInfo in columnsInfo" :key="columnInfo.columnName" class="col-md-3 mt-3">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ columnInfo.columnName }}</h5>
        <dl class="row">
          <dt class="col-sm-6">Type:</dt>
          <dd class="col-sm-6">{{ columnInfo.columnType }}</dd>

          <dt class="col-sm-6">Length:</dt>
          <dd class="col-sm-6">{{ columnInfo.lenColumn }}</dd>

          <dt class="col-sm-6">Distinct Values:</dt>
          <dd class="col-sm-6">{{ columnInfo.distinctValues }}</dd>

          <dt class="col-sm-6">Unique Values:</dt>
          <dd class="col-sm-6">{{ columnInfo.uniqueValues }}</dd>

          <dt class="col-sm-6">NaN Values:</dt>
          <dd class="col-sm-6">{{ columnInfo.nanValues }}</dd>

          <dt class="col-sm-6">Mean:</dt>
          <dd class="col-sm-6">{{ columnInfo.meanColumn }}</dd>

          <dt class="col-sm-6">Min:</dt>
          <dd class="col-sm-6">{{ columnInfo.minColumn }}</dd>

          <dt class="col-sm-6">Max:</dt>
          <dd class="col-sm-6">{{ columnInfo.maxColumn }}</dd>
        </dl>
      </div>
    </div>
  </div>
</div>

</template>

<script>
import basicDialogue  from './basicDialogue.vue'

export default {
    name: 'csvProfilerComponent',
    components:{
        basicDialogue
    },
    data() {
        return {
        errorVisible: false,
        csvUploadError: "",
        columnsInfo: [],
        csvProfilerForm:{
            csvSeperator: "",
            headerRow: "",
            quoteChar: "",
            csvFile: null
        }
    };
  },
  methods:{
    handleFileUpload(event) {
            const file = event.target.files[0]
            this.csvProfilerForm.csvFile = file;
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
            const response = await fetch("http://127.0.0.1:5000/csvProfiler", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            this.columnsInfo = [];
            this.errorVisible = true;
            this.csvUploadError = response.statusText;
            
        }
        else{
            this.columnsInfo = await response.json();
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