<template>
    <div class="col-2 h-100 sideHeader" align="center">
        <div class="btn-group-vertical pt-3">
            <RouterLink to="/" role="button" class="btn btn-secondary"><img class=" icon rounded img-fluid " src="../assets/Images/homeIcon.svg" alt="Home"></RouterLink>
            <RouterLink to="/csvProfiler" role="button" class="btn btn-secondary"><img class="icon rounded img-fluid " src="../assets/Images/fileIcon.svg" alt="FileUploader"></RouterLink >
            <RouterLink to="/connectionPage" role="button" class="btn btn-secondary"><img class="icon rounded img-fluid " src="../assets/Images/databaseIcon.svg" alt="Database"></RouterLink>
            <RouterLink to="/profilerPage" role="button" class="icon btn btn-secondary">Profiler</RouterLink>
            <RouterLink to="/tablePage" role="button" class="icon btn btn-secondary" >Tables</RouterLink>
            <RouterLink to="/settingsPage" role="button" class="icon btn btn-secondary"><img class="icon rounded img-fluid " src="../assets/Images/settingIcon.svg" alt="settings"></RouterLink>
        </div>
    </div>  
</template>

<style>
    .sideHeader{
        background-color: #5b5d62;
        border-right: 1px solid #dee2e6;
    }
    .btn{
        background-color: #5b5d62;
        border: 0px;
    }
    .icon{
        width: 75px; /* Adjust the width as needed */
        height: 75px; /* Adjust the height as needed */
    }
</style>
<script>
export default {
  name: 'sideHeader',
};
</script>

