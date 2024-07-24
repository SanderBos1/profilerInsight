<template>
    <div class="row bg-secondary text-white py-3">
        <div class="col-md-6">
            <div class="btn-group">
                <RouterLink to="/" role="button" class="btn btn-secondary">Home</RouterLink>
                <RouterLink to="/csvProfiler" role="button" class="btn btn-secondary">CSV Profiler</RouterLink >
                <RouterLink to="/profilerPage" role="button" class="btn btn-secondary">Profiler</RouterLink>
                <RouterLink to="/connectionPage" role="button" class="btn btn-secondary">Connections</RouterLink>
                <RouterLink to="/tablePage" role="button" class="btn btn-secondary" >Tables</RouterLink>
                <RouterLink to="/settingsPage" role="button" class="btn btn-secondary">Settings</RouterLink>
            </div>
        </div>
        <div class="col-md-6 text-end">
             <h1>Profiler Insight</h1>
         </div>
    </div>
</template>

<script>
export default {
  name: 'basicHeader',
};
</script>