<template>
    <div v-if="error" class="modal fade show" 
      tabindex="-1" aria-labelledby="exampleModalLabel" aria-modal="true" role="dialog" 
      style="display:block">
      
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
              <div class="col-md-11 col-sm-11">
                <h5 class="modal-title">{{ dialogTitle }}</h5>
              </div>
              <div class="col-md-1 col-sm-1">
                <button type="button"  @click="closeError()" :class='"closeDialogue btn btn-danger"' >X</button>
              </div>
          </div>
          <div class="modal-body">
           <slot name="dialogueBody"></slot>
          </div>
          <div class="modal-footer">
            <slot name="dialogueFooter"></slot>
          </div>
        </div>
      </div>
    </div>
  
  </template>
  
  <script>
  export default {
    name: 'errorDialogue',
    props: {
      error: String,
      dialogTitle:String
    },
    emits: ['closeError'],
    methods:{
      closeError(){
            this.$emit("closeError"); 
          },
    },
  
  }
  </script>
  
  <style>
  
  </style>