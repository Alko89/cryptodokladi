import Vue from "vue";
import App from "./App";
import router from "./router/index";

import PaperDashboard from "./plugins/paperDashboard";
import "vue-notifyjs/themes/default.css";

import BootstrapVue from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(PaperDashboard);
Vue.use(BootstrapVue);

/* eslint-disable no-new */
new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
