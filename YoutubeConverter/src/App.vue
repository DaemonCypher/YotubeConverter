<template>
  <YoutubeDownloader />
</template>

<script>
import YoutubeDownloader from './components/YoutubeDownloader.vue';

export default {
  name: 'App',
  components: {
    YoutubeDownloader,
  }
}
</script>

<style>
#app {
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
