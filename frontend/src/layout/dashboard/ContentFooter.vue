<template>
  <footer class="footer">
    <div class="container-fluid d-flex flex-wrap justify-content-between">
      <nav>
        <ul>
          <li>
            <router-link :to="{path:'/dashboard'}">Dashboard</router-link>
          </li>
        </ul>
      </nav>
      <div class="copyright d-flex flex-wrap">
        <a href="https://github.com/Alko89/cryptodokladi" target="_blank">CryptoDokladi.</a>
        &nbsp;by&nbsp;GoOpen&nbsp;
      </div>
    </div>
  </footer>
</template>
<script>
export default {};
</script>
<style>
</style>
