<template>
    <div class="container-fluid">
        <basicHeader></basicHeader>
        <div class="row">
          <router-view />
        </div> 
    </div>
  </template>
  
  <script>
  import basicHeader from './components/basicHeader.vue';
  
  export default {
    name: 'App',
    components: {
        basicHeader,
    }
  };
  </script>
  
  <style>
  /* Your global styles */
  </style>
  