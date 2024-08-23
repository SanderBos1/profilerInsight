<template>

    <!-- Main container row for the component -->
    <div class="row">

        <!-- Quality Overview -->
        <div class="col-sm-12 col-md-10 order-sm-2 order-md-1 text-sm-center text-center">
            <div class="row">
                <div class="col-md-6">
                    <div class="btn-group w-100" id="columnButton">
                        <button class="btn btn-primary grey" @click="returnTableOverview">Return</button>
                        <button class="btn btn-primary grey" @click="changeView">Data Profiler</button>
                        <button class="btn btn-primary grey" @click="calculateQuality" data-bs-toggle="tooltip" title="Checks all defined quality rules on your data, can take a while.">Calculate Quality</button>
                    </div>
                </div> 
            </div>  
            <div class="row">
                <h3> Quality Rules of {{ table_info.schema_name }}.{{ table_info.table_name }}</h3>
            </div>


            <!-- Quality Rules or No Rules Alert -->
            <div class="row">
                <div v-if="table_rules.length === 0" class="col-12">
                    <div class="alert alert-warning" role="alert">
                        No Quality Rules have been defined for this table. Feel free to add some.
                    </div>
                </div>
            <div v-else class="row">
                <div class="col-md-4" v-for="rule in table_rules" :key="rule.rule_id" >
                    <div class="card">
                        <div class="card-header row">
                            <h5 class="card-title col-md-10">{{ rule.quality_rule }} ({{ rule.column_name }})</h5>
                            <button class="btn btn-danger btn-sm col-md-2" @click="deleteRule(rule.rule_id)">X</button>
                        </div>
                        <div class="card-body" :style="getStatusStyle(rule.succeded)">
                            <p class="mb-1"><b>Threshold:</b> {{ rule.threshold }} %</p>        
                            <p class="mb-1"><b>Calculated:</b> {{ rule.calculated_threshold }} %</p>                            
                        </div>
                    </div>
                </div>
            </div>
        </div> 

            <div class="row">
                <div class="col-md-12">
                    <h3 class="mt-3">Add Quality Rule</h3>
                </div>
                <div class="row">
                    <div v-for="rule in rules" :key=rule.rule_id>
                        <ruleComponent :rule="rule" :table_id="table_id" :columns="columns" @reLoad="getTableRules"></ruleComponent>
                    </div>  
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

import ruleComponent from  '../qualityRuleComponents/ruleComponent.vue';

export default{

    name: "DbTableView",
    components:{
        ruleComponent
    },
    computed: {
        table_id() {
        return this.$route.params.table_id;
        }
    },
    data(){
        return{
            columns: [],
            error: "",
            table_rules: [],
            rules: [],
            table_info: {}
        }
    },
    mounted(){
        this.getQualityRules();
        this.getColumns();
        this.setTableInfo();
        this.getTableRules();
    },
    methods:{
        async calculateQuality(){
            const apiEndpoint = this.$API_ENDPOINTS.CALCULATE_QUALITY(this.table_id);
            await this.$fetchData(apiEndpoint, 'GET')
                .then((data) => {
                    if ("Error" in data) {
                        this.error = data["Error"]
                    }
                    else{
                        this.getTableRules()
                    }
            });   
        },
        changeView(){
            this.$router.push({path: `/DbTableView/${this.table_id}`})
        },
        closeError() {
            this.error = "";
        },
        async deleteRule(rule_id){
            const apiEndpoint = this.$API_ENDPOINTS.DELETE_QUALITY_RULE(rule_id);
            await this.$fetchData(apiEndpoint, 'DELETE')
                .then((data) => {
                    if ("Error" in data) {
                        this.error = data["Error"]
                    }
                    else{
                        this.getTableRules()
                    }
            });   
        },
        getStatusStyle(status){
            return{
                backgroundColor: status ? 'green' : 'red',
            }

        },
        async getTableRules(){
            const apiEndpoint = this.$API_ENDPOINTS.GET_QUALITY_RULES_TABLE(this.table_id);
            await this.$fetchData(apiEndpoint, 'GET')
                .then((data) => {
                    if ("Error" in data) {
                        this.error = data["Error"]
                    }
                    else{
                        this.table_rules = data["Answer"];
                    }
            });   
        },
        async getQualityRules() {
            const apiEndpoint = this.$API_ENDPOINTS.GET_QUALITY_RULES;
            await this.$fetchData(apiEndpoint, 'GET')
                .then((data) => {
                    if ("Error" in data) {
                        this.error = data["Error"]
                    }
                    else{
                        this.rules = data["Answer"];
                    }
            });     
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
    returnTableOverview(){
        this.$router.push({path: `/connectionOverview/${this.table_info.connection_id}`});
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