// Import Vue core library and createApp function
import { createApp } from 'vue';

// Import Vue Router
import { createRouter, createWebHistory } from 'vue-router';

// Import BootstrapVue and its styles
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css';


// Import your Vue components and App component
import App from './profilerInsight.vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faDatabase, faServer, faTable, faUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
//css
import './assets/css/main.css'; 

//views
import homePage from './components/views/homePage.vue';
import fileProfiler from './components/views/fileProfiler.vue';
import connectionPage from './components/views/connectionPage.vue';
import settingsPage from './components/views/settingsPage.vue';
import connectionOverview from './components/views/connectionOverview.vue';
import DbTableView from './components/views/DbTableView.vue';

//global components
import { fetchData } from './utils/globalFunctions.js';
import { API_ENDPOINTS } from './utils/endpoints';
import errorDialogue from './components/global/errorDialogue.vue';
import basicDialogue from './components/global/basicDialogue.vue';

// Create a Vue app instance
const app = createApp(App);


// Create a router instance
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: homePage },
    { path: '/fileProfiler', component: fileProfiler },
    { path: '/connectionPage', component: connectionPage },
    { path: '/settingsPage', component: settingsPage },
    {path: '/connectionOverview/:connection_id', component: connectionOverview},
    {path: '/DbTableView/:table_id', component: DbTableView}
  ]
});
library.add(faDatabase, faTable, faServer, faUser);
// Use the router instance in the app
app.use(router);

app.component('errorDialogue', errorDialogue);
app.component('basicDialogue', basicDialogue);
app.component('font-awesome-icon', FontAwesomeIcon);

app.config.globalProperties.$API_ENDPOINTS = API_ENDPOINTS;
app.config.globalProperties.$fetchData = fetchData;



// Mount the app
app.mount('#app');