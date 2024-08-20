<template>

    <div v-if="azureSQLDatabase" class="modal fade show" 
        tabindex="-1" aria-labelledby="exampleModalLabel" aria-modal="true" role="dialog" 
        style="display:block">

        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">

                <!-- Modal Header -->
                <div class="modal-header">
                    <div class="col-md-11 col-sm-11">
                        <h5 class="modal-title">Add Azure SQL Database Connection.</h5>
                    </div>
                    <div class="col-md-1 col-sm-1">
                        <button type="button"  @click="close()" :class='"closeDialogue btn btn-danger"' >X</button>
                    </div>
                </div>

                <!-- Modal Body -->
                <div class="modal-body">
                    <form v-on:submit.prevent="submitAzureSQLDBForm" id="addConnectionForm">
                        <div class="mb-3">
                            <label for="connectionId" class="form-label">Connection ID</label>
                            <input type="text" id="connectionId"  v-model="azuresqlForm.connection_id" class="form-control" data-bs-toggle="tooltip" title="A unique identifier of your connections">
                        </div>
                        <div class="mb-3">
                            <label for="host" class="form-label">server</label>
                            <input type="text" id="host" v-model="azuresqlForm.server" class="form-control" data-bs-toggle="tooltip" title="Where your database is hosted">
                        </div>
                        <div class="mb-3">
                            <label for="port" class="form-label">Port</label>
                            <input type="number" id="port" v-model="azuresqlForm.port" class="form-control" data-bs-toggle="tooltip" title="The port of your database server">
                        </div>
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <input type="text" id="username" v-model="azuresqlForm.username" class="form-control" data-bs-toggle="tooltip" title="The user that connects to the database, use an sql user, not an email adress">
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" id="password" v-model="azuresqlForm.password" class="form-control" data-bs-toggle="tooltip" title="The corresponding password">
                        </div>
                        <div class="mb-3">
                            <label for="database" class="form-label">Database</label>
                            <input type="text" id="database" v-model="azuresqlForm.database" class="form-control" data-bs-toggle="tooltip" title="Which database you want to connect to.">
                        </div>
                        <div class="mb-3">
                            <label for="db_type" class="form-label">db_type</label>
                            <input type="text" id="db_type" v-model="azuresqlForm.db_type" class="form-control" readonly data-bs-toggle="tooltip" title="Your chosen Database Type">
                        </div>  
                            <button class="btn btn-primary grey">Submit</button>
                    </form>
                </div>


                <!-- Modal footer -->
                <div class="modal-footer">
                    <button class="btn btn-primary grey" @click="returnBack()">Return</button>
                </div>
            </div>
        </div>

        <!-- Error Dialogue -->

        <errorDialogue :error="error"  @closeError="closeError" dialogTitle="Postgres Connection Error">
            <template v-slot:dialogueBody>
                <div class="col-md-12">
                    <p>{{ error }}</p>
                </div>
            </template>
        </errorDialogue>  
    </div>  

</template>

<script>

export default{

    name: "azureSQLDatabaseConnectionForm",
    props: {
        azureSQLDatabase: Boolean,
    },
    emits: ['connectionAdded', 'backToConnectionTypes', 'closeForm'],
    data(){
        return{
            error: "",
            azuresqlForm:{
                connection_id: '',
                server: '',
                port: '1433',
                username: '',
                password: '',
                database: '',
                db_type: 'azuresql',
            }
        }
    },
    methods:{
        close(){
            this.$emit('closeForm', "azuresql");
        },
        returnBack(){
            this.$emit('backToConnectionTypes', "azuresql");
        },
        closeError() {
            this.error = "";
        },
        async submitAzureSQLDBForm() {
            try {
                const response = await fetch(this.$API_ENDPOINTS.ADD_POSTGRES_CONNECTION, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(this.azuresqlForm)
            });

            if (!response.ok) {
                const data = await response.json();
                this.error = data["Error"];
            }
            else{
                this.$emit('connectionAdded', "azuresql");
                this.close();
                }
        
        }
        catch (error) {
            this.error = error;
        }
    },
        
    }
}

</script>