<template>
  <div class="about">
    <h1 v-for="t in tokens" :key="t.id">
      {{ t.name }}
    </h1>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      tokens: [
        {name: 'Bitcoin'},
        {name: 'PIVX'}
      ]
    }
  },
  mounted() {
    axios.get("/api/tokens")
    .then(response => {
      this.tokens = response.data
    })
  }
}
</script>
