<template>
  <nav class="navbar navbar-expand-lg navbar-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">{{routeName}}</a>
      <button class="navbar-toggler navbar-burger"
              type="button"
              @click="toggleSidebar"
              :aria-expanded="$sidebar.showSidebar"
              aria-label="Toggle navigation">
        <span class="navbar-toggler-bar"></span>
        <span class="navbar-toggler-bar"></span>
        <span class="navbar-toggler-bar"></span>
      </button>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ml-auto">
          <li v-if="!loggedIn" class="nav-item">
            <router-link class="nav-link" :to="{path:'/register'}">
              <i class="ti-pencil"></i>
              <p>
                {{ $loggedIn }}
              </p>
            </router-link>
          </li>
          <li v-if="!loggedIn" class="nav-item">
            <router-link class="nav-link" :to="{path:'/login'}">
              <i class="ti-user"></i>
              <p>
                Login
              </p>
            </router-link>
          </li>
          <li v-if="loggedIn" class="nav-item">
            <router-link class="nav-link" :to="{path:'/logout'}">
              <i class="ti-user"></i>
              <p>
                Logout
              </p>
            </router-link>
          </li>
        </ul>
      </div>
    </div></nav>
</template>
<script>
import auth from "@/auth/auth.js"

export default {
  components: {
  },
  computed: {
    routeName() {
      const { name } = this.$route;
      return this.capitalizeFirstLetter(name);
    }
  },
  data() {
    return {
      activeNotifications: false,
      loggedIn: auth.loggedIn()
    };
  },
  methods: {
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    toggleNotificationDropDown() {
      this.activeNotifications = !this.activeNotifications;
    },
    closeDropDown() {
      this.activeNotifications = false;
    },
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    hideSidebar() {
      this.$sidebar.displaySidebar(false);
    }
  }
};
</script>
<style>
</style>
