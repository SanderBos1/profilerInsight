<template>
    <div v-if="OpenClose" class="modal fade show" 
        tabindex="-1" aria-labelledby="exampleModalLabel" aria-modal="true" role="dialog" 
        style="display:block">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title">{{ dialogTitle }}</h5>
        </div>
        <div class="modal-body">
         <slot name="dialogueBody"></slot>
        </div>
        <div class="modal-footer">
          <slot name="dialogueFooter"></slot>
          <button type="button"  @click="OpenCloseFun()" :class="'btn btn-'+variant" >close</button>
        </div>
      </div>
    </div>
  </div>
  </template>

<script>
export default {
  name: 'basicDialogue',
  props: {
    visible: Boolean,
    variant:String,
    dialogTitle:String
  },
  data(){
    return{
       OpenClose:this.visible
    }
  },
  methods:{
        OpenCloseFun(){
           this.OpenClose = false;
           this.$emit('update:visible', false); 
        },
  },
  watch: { 
      visible: function(newVal) { 
        this.OpenClose = newVal;
      }
    }

}
</script>