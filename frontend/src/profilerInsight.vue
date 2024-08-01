<template>
  <div class="row">
    <baseHeader></baseHeader>
  </div>
  <div class="row h-100">
    <baseSideHeader></baseSideHeader>
    <div class="col-10 p-3">
      <router-view />
    </div> 
</div>

  </template>
  
  <script>
  import baseSideHeader from './components/baseSideHeader.vue';
  import baseHeader from './components/baseHeader.vue';

  export default {
    name: 'App',
    components: {
      baseSideHeader,
      baseHeader
    }
  };
  </script>
