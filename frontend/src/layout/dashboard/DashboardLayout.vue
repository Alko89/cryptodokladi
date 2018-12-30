<template>
  <div class="wrapper">
    <side-bar>
      <template slot="links">
        <sidebar-link to="/dashboard" name="Dashboard" icon="ti-panel"/>
        <sidebar-link to="/profile" name="User Profile" icon="ti-user"/>
        <sidebar-link to="/table-list" name="Transactions" icon="ti-view-list-alt"/>
        <sidebar-link to="/about" name="About" icon="ti-info"/>
      </template>
      <mobile-menu>
        <li v-if="!isLoggedIn" class="nav-item">
          <router-link class="nav-link" :to="{path:'/register'}">
            <i class="ti-pencil"></i>
            <p>Register</p>
          </router-link>
        </li>
        <li v-if="!isLoggedIn" class="nav-item">
          <router-link class="nav-link" :to="{path:'/login'}">
            <i class="ti-user"></i>
            <p>Login</p>
          </router-link>
        </li>
        <li v-else class="nav-item">
          <a href="#" class="nav-link" @click="logout">
            <i class="ti-user"></i>
            <p>Logout</p>
          </a>
        </li>
        <li class="divider"></li>
      </mobile-menu>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click.native="toggleSidebar"></dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<style lang="scss">
</style>
<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "./MobileMenu";

export default {
  components: {
    TopNavbar,
    ContentFooter,
    DashboardContent,
    MobileMenu
  },
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isLoggedIn;
    }
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    },
    logout: function() {
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
      });
    }
  }
};
</script>
