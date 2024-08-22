<template>
    <component :is="component" :rule="rule" :table_id="table_id" :columns="columns" @reLoad="emit_signal"></component>

</template>
  
  

<script>

import emptyValuesRuleComponent from  "../qualityRuleComponents/emptyValuesRuleComponent.vue"; 
import patternRuleComponent from  "../qualityRuleComponents/patternRuleComponent.vue";
import { markRaw } from 'vue';

export default{

  name: "ruleComponent",
  components:{
        emptyValuesRuleComponent
    },
  onMounted(){
        this.component = this.rule_converter[this.type];
    },
  props:{
        rule: Object,
        table_id: String,
        columns: Array,
        type: String

    },
data(){
  return{
    component: emptyValuesRuleComponent,
    rule_converter: {
      "No Empty Rule": markRaw(emptyValuesRuleComponent),
      "Match Pattern Rule": markRaw(patternRuleComponent),
    }
  }
  },
  emits : ['reLoad'],

  methods:{
    emit_signal(){
        this.$emit('reLoad');
    },
  }
}
</script>