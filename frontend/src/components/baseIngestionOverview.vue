<template>
    <div v-if="columnInfo" class="card">
      <div class="card-body">
        <h5 class="card-title">{{ columnInfo.columnName }}</h5>
        <dl class="row">
          <dt class="col-sm-6">Type:</dt>
          <dd class="col-sm-6">{{ columnInfo.columnType }}</dd>

          <dt class="col-sm-6">Length:</dt>
          <dd class="col-sm-6">{{ columnInfo.lenColumn }}</dd>

          <dt class="col-sm-6">Distinct Values:</dt>
          <dd class="col-sm-6">{{ columnInfo.distinctValues }}</dd>

          <dt class="col-sm-6">Unique Values:</dt>
          <dd class="col-sm-6">{{ columnInfo.uniqueValues }}</dd>

          <dt class="col-sm-6">NaN Values:</dt>
          <dd class="col-sm-6">{{ columnInfo.nanValues }}</dd>

          <dt class="col-sm-6">Mean:</dt>
          <dd class="col-sm-6">{{ columnInfo.meanColumn }}</dd>

          <dt class="col-sm-6">Min:</dt>
          <dd class="col-sm-6">{{ columnInfo.minColumn }}</dd>

          <dt class="col-sm-6">Max:</dt>
          <dd class="col-sm-6">{{ columnInfo.maxColumn }}</dd>
        </dl>
      </div>
    </div>
</template>

<script>
export default {
    name: 'baseIngestionOverview',
    props: {
        columnInfo: Object
    }
}       
    
</script>