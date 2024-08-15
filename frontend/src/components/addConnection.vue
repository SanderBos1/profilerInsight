<template>
    
    <div class="offset-md-10">
        <button class="btn btn-secondary" @click="showConnectionTypes=true" data-bs-toggle="tooltip" title="Define a connection to a database" >Add Connection</button>    
    </div>

    <basicDialogue :visible="showConnectionTypes" @update:visible="showConnectionTypes = $event" dialogTitle="Choose Connection Type">
        <template v-slot:dialogueBody>
            <div class="row">
                <div class="col-4">
                    <img src="../assets/Images/postgresLogo.jpg" @click="postgres=true" class="img-thumbnail" alt="Postgres Logo">
                </div>
            </div>
        </template>
    </basicDialogue>
    <postgresConnectionForm :postgres=postgres @closePostgres="closePostgres" @backToConnectionTypes="returnBack" @conncetionAdded="conncetionAdded"></postgresConnectionForm>
</template>


<script>
import postgresConnectionForm from './postgresConnectionForm.vue';

export default {

    name: "addConncetion",
    components: {
        postgresConnectionForm
    },
    data() {
        return {
            showConnectionTypes: false,
            postgres: false,
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
    closePostgres(){
        this.postgres = false;
        this.showConnectionTypes = false;
    },
    returnBack(connectionType){
        if(connectionType == "postgres"){
            this.postgres = false;
            this.showConnectionTypes = true;
        }
    },
    conncetionAdded(){
        this.$emit('loadConnections');
        this.$emit('ingestTables');
    }
}
       
}

</script>