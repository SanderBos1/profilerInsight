<template>
    <div v-if="columnInfo" class="row">
      <h2 align="center">{{ columnInfo.columnName }}</h2>
      <div class="row">
        <div class="col-md-4   h-100">
            <h5 align="center" >Base overview</h5>
            <div class="card">
              <div class="card-body">
                <div class="row">
                  <div class='col-md-6'>
                    <dt >Type:</dt>
                    <dd >{{ columnInfo.columnType }}</dd>
                  </div>
                  <div class='col-md-6'>
                    <dt >Length:</dt>
                    <dd >{{ columnInfo.lenColumn }}</dd>
                  </div>  
                </div>
                <div class="row">
                  <div class='col-md-6'>
                    <dt >Distinct Values:</dt>
                    <dd >{{ columnInfo.distinctValues }}</dd>
                  </div>
                  <div class='col-md-6'>
                    <dt >Unique Values:</dt>
                    <dd >{{ columnInfo.uniqueValues }}</dd>
                  </div>  
                </div>
            </div>
          </div>
        </div>
        <div class="col-md-3 ">
          <div class=" h-100">
            <basePieChart :values="[columnInfo.nanValues, 100-columnInfo.nanValues]"  :labels = "['NanValues', 'Values']" :backgroundColor="['#5b5d62', '#fe5000']"></basePieChart>
            <dt  align="center">NaN Values:</dt>
            <dd  align="center">{{ columnInfo.nanValues }}</dd>
          </div>
        </div>
        <div v-if="'baseStats' in columnInfo"  class="col-md-4   h-100">
            <h5 align="center"> Base statistics</h5>
            <div class="card">
              <div class="card-body">
                <div class="row">
                  <div class="col-md-6">
                    <dt >Mean:</dt>
                    <dd >{{ columnInfo.baseStats.meanColumn }}</dd>
                  </div>
                  <div class="col-md-6">
                    <dt >Median:</dt>
                    <dd >{{ columnInfo.baseStats.medianColumn }}</dd>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6">
                    <dt >Min:</dt>
                    <dd >{{ columnInfo.baseStats.minColumn }}</dd>
                  </div>
                  <div class="col-md-6">
                    <dt >Max:</dt>
                    <dd >{{ columnInfo.baseStats.maxColumn }}</dd>
                  </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="'numericImages' in columnInfo">
        <div class="row pt-3">
        <h5 align="center"> Distribution</h5>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <dd align="center">
                <img v-bind:src="'data:image/jpeg;base64,'+columnInfo.numericImages.histogram" alt="histogramImage" class=img-fluid/>
              </dd>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-body">
              <dd align="center">
                <img v-bind:src="'data:image/jpeg;base64,'+columnInfo.numericImages.boxplot" alt="boxplot"  class=img-fluid/>
              </dd>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import basePieChart from './basePieChart.vue';

export default {
  name: 'baseIngestionOverview',
  props: {
      columnInfo: Object
  },

  components:{
    basePieChart
  },

}       
    
</script>