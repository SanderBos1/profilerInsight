<template>
    <div class="container mt-3" style= "max-height: 400px; overflow-y: auto;">
      <div class="card p-3 shadow-sm">
        <div class="card-body">
          <div class="row mb-3">
            <div class="col-md-6">
                <h5> {{ rule.name }}</h5>
                <p class="card-text text-muted">{{ rule.description }}</p>
            </div>
            <div class="col-md-6">
                <div class="mb-2">
                    <label for="pattern" class="form-label">Pattern:</label>
                    <input type="text" id="pattern" v-model="qualityForm.extra_info" class="form-control form-control-sm" aria-describedby="threshold-help"/>
                </div>
                <div class="mb-2">
                    <label for="threshold" class="form-label">Threshold:</label>
                    <input type="number" id="threshold" v-model="qualityForm.threshold" class="form-control form-control-sm" aria-describedby="threshold-help"/>
                </div>
                <div class="mb-2">
                  <label for="column-select" class="form-label">Column:</label>
                  <select id="column-select" v-model="qualityForm.column_name" class="form-select form-select-sm" aria-label="Select a column">
                  <option disabled value="">Select a column</option>
                  <option v-for="column in columns" :key="column" :value="column">
                    {{ column }}
                  </option>
                </select>
              </div>
            </div>
          </div>
            <button class="btn btn-primary btn-sm grey" @click="addQualityRule">
                Add Quality Rule
            </button>
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

export default{

    name: "emptyValuesRuleComponent",
    props:{
        rule: Object,
        table_id: String,
        columns: Array,
    },
    emits : ['reLoad'],
    data(){
        return{
            error: "",
            qualityForm:{
                table_id: this.table_id,
                rule_name: this.rule.name,
                column_name: "",
                threshold: 0,
                extra_info: ""

            }
        }
    },
    methods:{
        async addQualityRule() {
            try {
                const response = await fetch(this.$API_ENDPOINTS.ADD_QUALITY_RULE, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                    },
                body: JSON.stringify(this.qualityForm)
                });

                if (!response.ok) {
                    const data = await response.json();
                    this.error = data["Error"];
                }
                else {
                    this.$emit('reLoad');
                }

            }
            catch (error) {
                this.error = error;
            }
        },
      closeError() {
        this.error = "";
      },
    },


}

</script>