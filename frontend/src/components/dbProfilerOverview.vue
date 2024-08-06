<template>
    
    <div class="row">

    <!-- Overview Section -->

        <div class="col-md-6 col-sm-12">
            <div class="card mt-3">
                <div class="card-header text-center grey">
                    <h5>Overview</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mt-3">
                            <dt>Type:</dt>
                            <dd>{{profilerOverview.column_type}}</dd>
                        </div>
                        <div class="col-md-6 mt-3">
                            <dt>Colum Length:</dt>
                            <dd>{{profilerOverview.column_length}}</dd>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mt-3">
                            <dt>Median:</dt>
                            <dd>{{profilerOverview.median_value}}</dd>
                        </div>
                        <div class="col-md-6 mt-3">
                            <dt>Mean:</dt>
                            <dd>{{profilerOverview.mean_value}}</dd>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mt-3">
                            <dt>Min:</dt>
                            <dd>{{profilerOverview.min_value}}</dd>
                        </div>
                        <div class="col-md-6 mt-3">
                            <dt>Max:</dt>
                            <dd>{{profilerOverview.max_value}}</dd>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-6 mt-3">
                            <dt>Distinct:</dt>
                            <dd>{{profilerOverview.number_distinct}}</dd>
                        </div>
                        <div class="col-md-6 mt-3">
                            <dt>Unique_values:</dt>
                            <dd>{{profilerOverview.number_unique}}</dd>
                        </div>
                    </div>
                </div>
            </div>
        </div>


    <!-- NaN Section -->
        <div class="col-sm-12 col-md-6">
            <basePieChart
            :values="[profilerOverview.number_nans, 100 - profilerOverview.number_nans]"
            :labels="['NanValues', 'Values']"
            :backgroundColor="['#5b5d62', '#fe5000']"
            ></basePieChart>
            <dt align="center">NaN Values:</dt>
            <dd align="center">{{ profilerOverview.number_nans }}</dd>
        </div>


    <!-- Distribution images section -->
        <div v-if="profilerOverview.histogram !== undefined && profilerOverview.histogram !== null">
            <div class="row pt-3">
                <h5 align="center">Distribution</h5>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <dd align="center">
                                <img
                                v-bind:src="'data:image/jpeg;base64,' + profilerOverview.histogram"
                                alt="histogramImage"
                                class="img-fluid"
                                >
                            </dd>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <dd align="center">
                                <img
                                v-bind:src="'data:image/jpeg;base64,' + profilerOverview.boxplot"
                                alt="boxplot"
                                class="img-fluid"
                                >
                            </dd>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        
      <!-- Data Patterns section -->
    <div v-if="profilerOverview.patterns !== undefined && profilerOverview.patterns !== null">
      <div class="col-md-12">
        <div class="card mt-3">
          <div class="card-header text-center grey" data-bs-toggle="tooltip" title="Show which patterns there are in your data. A represent a letter, 1 a number and & a special characters. The characters . , @ and / represent themself.">
            <h5>Data Patterns</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <table class="table table-striped table-hover">
                <thead>
                  <tr>
                    <th scope="col">Pattern</th>
                    <th scope="col">Number of Rows</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(pattern, index) in profilerOverview.patterns" :key="index">
                    <td>
                      {{ pattern[0] }}
                    </td>
                    <td>
                      {{ pattern[1] }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

        <!-- Data Preview section -->
        <div class="row pt-3">
            <div class="col-md-12">
                <div class="card mt-3">
                    <div class="card-header text-center grey">
                    <h5>Data Preview</h5>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-12 overflow-auto">
                                <div v-html="profilerOverview.data_preview"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import basePieChart from './basePieChart.vue';

export default{


    name: 'dbProfilerOverview',
    components: {
        basePieChart
    },
    props: {
        profilerOverview: Object
    }

}

</script>