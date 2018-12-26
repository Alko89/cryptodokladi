import Notify from "vue-notifyjs";
import SideBar from "@/components/SidebarPlugin";
import GlobalComponents from "./globalComponents";
import GlobalDirectives from "./globalDirectives";
import "es6-promise/auto";

import BootstrapVue from 'bootstrap-vue';

//css assets
import "bootstrap/dist/css/bootstrap.css";
import "@/assets/sass/paper-dashboard.scss";
import "@/assets/css/themify-icons.css";

import 'bootstrap-vue/dist/bootstrap-vue.css';
import "cryptofont/css/cryptofont.min.css";

export default {
  install(Vue) {
    Vue.use(GlobalComponents);
    Vue.use(GlobalDirectives);
    Vue.use(SideBar);
    Vue.use(Notify);

    Vue.use(BootstrapVue);
  }
}
