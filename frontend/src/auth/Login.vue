<template>
  <div class="row">
    <div class="col-md-4">
      <card class="card" title="Login">
        <div>
    <p v-if="$route.query.redirect">
      You need to login first.
    </p>
    
          <form @submit.prevent>
            
            <div class="row">
              <div class="col-md-12">
                <fg-input type="text"
                          label="Address"
                          placeholder="Home Address"
                          v-model="email">
                </fg-input>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12">
                <fg-input type="text"
                          label="Address"
                          placeholder="Home Address"
                          v-model="pass">
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
import auth from './auth'

export default {
  data () {
    return {
      email: '',
      pass: '',
      error: false
    }
  },
  methods: {
    login () {
      auth.login(this.email, this.pass, loggedIn => {
        if (!loggedIn) {
          this.error = true
        } else {
          this.$router.replace(this.$route.query.redirect || '/')
        }
      })
    }
  }
}
</script>

<style>
.error {
  color: red;
}
</style>
