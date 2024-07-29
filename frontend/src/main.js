// Import Vue core library and createApp function
import { createApp } from 'vue';

// Import Vue Router
import { createRouter, createWebHistory } from 'vue-router';

// Import BootstrapVue and its styles
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.css';

// Import your Vue components and App component
import App from './profilerInsight.vue';



//views
import homePage from './components/views/homePage.vue';
import csvProfiler from './components/views/csvProfiler.vue';
import connectionPage from './components/views/connectionPage.vue';
import profilerPage from './components/views/profilerPage.vue';
import settingsPage from './components/views/settingsPage.vue';
import tablePage from './components/views/tablePage.vue';

// Create a Vue app instance
const app = createApp(App);


// Create a router instance
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: homePage },
    { path: '/csvProfiler', component: csvProfiler },
    { path: '/connectionPage', component: connectionPage },
    { path: '/profilerPage', component: profilerPage },
    { path: '/settingsPage', component: settingsPage },
    { path: '/tablePage', component: tablePage }
  ]
});

// Use the router instance in the app
app.use(router);



// Mount the app
app.mount('#app');