<template>
  <component :is="currentComponent" :rule="rule" :table_id="table_id" :columns="columns" @reLoad="emit_signal"></component>
</template>

<script>
import emptyValuesRuleComponent from  "../qualityRuleComponents/emptyValuesRuleComponent.vue"; 
import patternRuleComponent from  "../qualityRuleComponents/patternRuleComponent.vue";
import { markRaw } from 'vue';

export default {
  name: "ruleComponent",
  components: {
    emptyValuesRuleComponent,
    patternRuleComponent
  },
  props: {
    rule: Object,
    table_id: String,
    columns: Array,
  },
  data() {
    return {
      rule_converter: {
        "No Empty Rule": markRaw(emptyValuesRuleComponent),
        "Match Pattern Rule": markRaw(patternRuleComponent),
      }
    };
  },
  computed: {
    currentComponent() {
      return this.rule_converter[this.rule.name] || null;
    }
  },
  emits: ['reLoad'],
  methods: {
    emit_signal() {
      this.$emit('reLoad');
    },
  }
}
</script>
