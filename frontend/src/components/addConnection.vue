<template>
    
    <div class="offset-md-10">
        <button class="btn btn-secondary" @click="showConnectionTypes=true" data-bs-toggle="tooltip" title="Define a connection to a database" >Add Connection</button>    
    </div>

    <basicDialogue :visible="showConnectionTypes" @update:visible="showConnectionTypes = $event" dialogTitle="Choose Connection Type">
        <template v-slot:dialogueBody>
            <div class="row">
                <div class="col-4">
                    <img src="../assets/Images/postgresLogo.jpg" @click="postgres=true" class="img-fluid" alt="Postgres Logo">
                </div>
                <div class="col-4">
                    <img src="../assets/Images/azureSQLDatabaseIcon.svg" @click="azureSQLDatabase=true" class="img-fluid" alt="Postgres Logo">
                </div>
            </div>
        </template>
    </basicDialogue>
    <postgresConnectionForm :postgres=postgres @closeForm="closeForm" @backToConnectionTypes="returnBack" @connectionAdded="conncetionAdded"></postgresConnectionForm>
    <azureSQLDatabaseConnectionForm :azureSQLDatabase=azureSQLDatabase @closeForm="closeForm" @backToConnectionTypes="returnBack" @connectionAdded="conncetionAdded"></azureSQLDatabaseConnectionForm>

</template>


<script>
import postgresConnectionForm from './postgresConnectionForm.vue';
import azureSQLDatabaseConnectionForm from './azureSQLDatabaseConnectionForm.vue';
export default {

    name: "addConncetion",
    components: {
        postgresConnectionForm,
        azureSQLDatabaseConnectionForm
    },
    data() {
        return {
            showConnectionTypes: false,
            postgres: false,
            azureSQLDatabase:false,
            postgresConnectionForm:{
                connection_id: "",
                host: "",
                port: "",
                username: "",
                password: "",
                database: "",
                db_type: "postgres"
            }
        }
    },
    emits: ['loadConnections', 'ingestTables'],
    methods: {
    closeForm(connectionType){
        if(connectionType == "postgres"){
            this.postgres = false;
        }
        if(connectionType == "azuresql"){
            this.azureSQLDatabase = false;
        }
        this.showConnectionTypes = false;
    },
    returnBack(connectionType){
        if(connectionType == "postgres"){
            this.postgres = false;
        }
        if(connectionType == "azuresql"){
            this.azureSQLDatabase = false;
        }
        this.showConnectionTypes = true;

    },
    conncetionAdded(){
        this.$emit('loadConnections');
        this.$emit('ingestTables');
    }
}
       
}

</script>