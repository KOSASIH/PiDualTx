<template>
  <div id="godchain-app">
    <header class="header">
      <h1>🌏 Cijoho Genesis God-Chain</h1>
      <p>ID 314159 | Ti Cijoho Pikeun Dunia | -6.979,108.484</p>
    </header>
    <main>
      <router-view />
    </main>
    <footer>
      <p>PiDualTx Dual Value System | GCV $314,159 + Market Price</p>
      <p>Warung Pi #0 - Capital of Peradaban</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#godchain-app {
  font-family: 'Inter', sans-serif;
  text-align: center;
  background: #0a0a0f;
  color: #00ffc3;
  min-height: 100vh;
}
.header { padding: 40px; border-bottom: 1px solid #00ffc3; }
footer { padding: 20px; font-size: 12px; opacity: 0.7; margin-top: 50px; }
</style>
