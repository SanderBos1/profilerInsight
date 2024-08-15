<template>

    <div v-if="postgres" class="modal fade show" 
        tabindex="-1" aria-labelledby="exampleModalLabel" aria-modal="true" role="dialog" 
        style="display:block">

        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">

                <!-- Modal Header -->
                <div class="modal-header">
                    <div class="col-md-11 col-sm-11">
                        <h5 class="modal-title">{{ dialogTitle }}</h5>
                    </div>
                    <div class="col-md-1 col-sm-1">
                        <button type="button"  @click="close()" :class='"closeDialogue btn btn-danger"' >X</button>
                    </div>
                </div>

                <!-- Modal Body -->
                <div class="modal-body">
                    <form v-on:submit.prevent="submitPostgressForm" id="addConnectionForm">
                        <div class="mb-3">
                            <label for="connectionId" class="form-label">Connection ID</label>
                            <input type="text" id="connectionId"  v-model="postgresConnectionForm.connection_id" class="form-control" data-bs-toggle="tooltip" title="A unique identifier of your connections">
                        </div>
                        <div class="mb-3">
                            <label for="host" class="form-label">server</label>
                            <input type="text" id="host" v-model="postgresConnectionForm.server" class="form-control" data-bs-toggle="tooltip" title="Where your database is hosted">
                        </div>
                        <div class="mb-3">
                            <label for="port" class="form-label">Port</label>
                            <input type="number" id="port" v-model="postgresConnectionForm.port" class="form-control" data-bs-toggle="tooltip" title="The port of your database server">
                        </div>
                        <div class="mb-3">
                            <label for="username" class="form-label">Username</label>
                            <input type="text" id="username" v-model="postgresConnectionForm.username" class="form-control" data-bs-toggle="tooltip" title="The user that connects to the databgase">
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password</label>
                            <input type="password" id="password" v-model="postgresConnectionForm.password" class="form-control" data-bs-toggle="tooltip" title="The corresponding password">
                        </div>
                        <div class="mb-3">
                            <label for="database" class="form-label">Database</label>
                            <input type="text" id="database" v-model="postgresConnectionForm.database" class="form-control" data-bs-toggle="tooltip" title="Which database you want to connect to.">
                        </div>        
                        <div class="mb-3">
                            <label for="db_type" class="form-label">db_type</label>
                            <input type="text" id="db_type" v-model="postgresConnectionForm.db_type" class="form-control" readonly data-bs-toggle="tooltip" title="Your chosen Database Type">
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

    name: "postgresConnectionForm",
    props: {
        postgres: Boolean,
    },
    emits: ['closePostgres', 'backToConnectionTypes', 'conncetionAdded'],
    data(){
        return{
            error: "",
            postgresConnectionForm:{
                connection_id: '',
                server: '',
                port: '',
                username: '',
                password: '',
                database: '',
                db_type: 'postgres'
            }
        }
    },
    methods:{
        close(){
            this.$emit('closePostgres', false);
        },
        returnBack(){
            this.$emit('backToConnectionTypes', "postgres");
        },
        closeError() {
            this.error = "";
        },
        async submitPostgressForm() {
            try {
                const response = await fetch(this.$API_ENDPOINTS.ADD_POSTGRES_CONNECTION, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(this.postgresConnectionForm)
            });

            if (!response.ok) {
                const data = await response.json();
                this.error = data["Error"];
            }
            else{
                this.$emit('conncetionAdded');
                this.close();
                }
        
        }
        catch (error) {
            this.errorVisible = true;
            this.error = error;
        }
    },
        
    }
}

</script>