<template>
  <div class="row">
    <div class="col-md-4">
      <card class="card" title="Login">
        <div>
    <p v-if="$route.query.redirect">
      You need to login first.
    </p>
    
          <form @submit.prevent="login">
            
            <div class="row">
              <div class="col-md-12">
                <fg-input type="text"
                          label="Name"
                          placeholder="Name"
                          v-model="email">
                </fg-input>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12">
                <fg-input type="password"
                          label="Password"
                          placeholder="Password"
                          v-model="password">
                </fg-input>
              </div>
            </div>

            <div class="text-center">
              <p-button type="info"
                        round
                        @click.native.prevent="login">
                Login
              </p-button>
            </div>
            <div class="clearfix"></div>
          </form>
        </div>
      </card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    login: function() {
      let email = this.email;
      let password = this.password;
      this.$store
        .dispatch("login", { email, password })
        .then(() => this.$router.push("/"))
        .catch(err => this.$notify({
          message: "Wrong username or password.",
          icon: "ti-info",
          horizontalAlign: "center",
          verticalAlign: "top",
          type: "danger"
        }));
    }
  }
};
</script>

<style>
.error {
  color: red;
}
</style>
