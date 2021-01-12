<template>
  <div class="app">
    <router-view />
  </div>
</template>

<style>
  @font-face {
    font-family: 'JetBrainsMono';
    src: url('assets/webfonts/JetBrainsMono-Regular.woff2') format('woff2')
  }

  * {
    font-family: 'JetBrainsMono', serif;
    margin: 0;
    padding: 0;
  }

  body {
    background-color: #101010;
    color: white;
    overflow: hidden;
  }
</style>
