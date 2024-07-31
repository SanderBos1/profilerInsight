<template>
    <div class="col-2 h-100 sideHeader" align="center">
        <div class="btn-group-vertical pt-3 sideHeaderButtons">
            <RouterLink to="/" role="button" class="grey border-0 btn btn-secondary" data-bs-toggle="tooltip" data-bs-placement="right" title="Go to the Home Page">
                <div class=" icon"><img class="rounded img-fluid " src="../assets/Images/homeIcon.svg" alt="Home"> 
                    <p>Home</p> 
                </div>
            </RouterLink>
            <RouterLink to="/csvProfiler" role="button" class="grey border-0 btn btn-secondary">
                <div class=" icon">
                    <img class="icon rounded img-fluid " src="../assets/Images/fileIcon.svg" alt="FileUploader" data-bs-toggle="tooltip" data-bs-placement="right" title="Go to the CSV Profiler Page">
                    <p>CSV Profiler</p>
                </div>
            </RouterLink >
            <RouterLink to="/connectionPage" role="button" class="grey border-0 btn btn-secondary">
                <div class=" icon">
                    <img class="icon rounded img-fluid " src="../assets/Images/databaseIcon.svg" alt="Database">
                    <p>Connections</p>
                </div>
            </RouterLink>
            <RouterLink to="/profilerPage" role="button" class="grey border-0 icon btn btn-secondary">
                <div class=" icon"><img class="icon rounded img-fluid " src="" alt="Table">
                    <p>Tables</p>
                </div>
            </RouterLink>
            <RouterLink to="/tablePage" role="button" class="grey border-0 icon btn btn-secondary" >
                <div class=" icon">
                    <img class="icon rounded img-fluid " src="" alt="Profiler">
                    <p>Database Profiler</p>
                </div>
            </RouterLink>
            <RouterLink to="/settingsPage" role="button" class="grey border-0 icon btn btn-secondary">
                <div class=" icon">
                    <img class="icon rounded img-fluid " src="../assets/Images/settingIcon.svg" alt="settings">
                    <p>Settings</p>
                </div></RouterLink>
        </div>
    </div>  
</template>

<style>
    .sideHeaderButtons{
        max-width: 100%;
    }
    .sideHeader{
        background-color: #5b5d62;
        border-right: 1px solid #dee2e6;
    }
    .icon{
        width:100%;
    }
    .icon img{
        max-width: 100px; 
        max-height: 100px;
        width: 100%; 
        height: auto;
    }
    .icon p{
        max-width: 100px; 
        max-height: 100px;
        width: 100%; 
        height: auto; 
        overflow: hidden; 
        text-overflow: ellipsis; 
        white-space: nowrap;
    }
</style>
<script>
export default {
  name: 'sideHeader',
};
</script>

