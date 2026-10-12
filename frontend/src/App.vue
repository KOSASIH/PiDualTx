<template>
  <div id="godchain-portal">
    <canvas ref="canvasRef" id="cosmic-canvas"></canvas>

    <div class="overlay">
      <header class="hero">
        <div class="badge">🌍 LIVE ON VERCEL</div>
        <h1 class="glitch" data-text="Cijoho Genesis">Cijoho Genesis<br><span>God-Chain</span></h1>
        <p class="coords">ID 314159 | Ti Cijoho Pikeun Dunia | -6.979,108.484</p>

        <div class="dual-box">
          <div class="dual-item gcv">
            <span class="label">SYMBOLIC GCV</span>
            <span class="value">$314,159</span>
          </div>
          <div class="divider"></div>
          <div class="dual-item market">
            <span class="label">MARKET PRICE</span>
            <span class="value" id="marketPrice">$0.00</span>
          </div>
        </div>
      </header>

      <main class="content">
        <div class="card genesis">
          <h3>🏛️ Warung Pi #0</h3>
          <p>Capital of Civilization — Genesis Block of Cijoho</p>
          <div class="status">
            <span class="dot"></span> God-Chain Active
          </div>
        </div>

        <div class="grid">
          <div class="card">
            <h4>PiDualTx System</h4>
            <p>Dual Value Consensus Engine</p>
          </div>
          <div class="card">
            <h4>Stellar SDK</h4>
            <p>Connected to Pi Network</p>
          </div>
        </div>

        <router-view />
      </main>

      <footer>
        <p>© 2026 Cijoho Genesis | KOSASIH - Bapak Peradaban Cijoho</p>
        <p class="small">No Official Pi Price - Community Consensus Value</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import * as THREE from 'three'
import gsap from 'gsap'

const canvasRef = ref(null)

onMounted(() => {
  // THREE.JS COSMIC BACKGROUND
  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  const renderer = new THREE.WebGLRenderer({ canvas: canvasRef.value, alpha: true, antialias: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(window.devicePixelRatio)

  // Stars
  const starsGeometry = new THREE.BufferGeometry()
  const starsCount = 3000
  const posArray = new Float32Array(starsCount * 3)
  for(let i=0; i<starsCount*3; i++) posArray[i] = (Math.random()-0.5)*2000
  starsGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3))
  const starsMaterial = new THREE.PointsMaterial({ size: 1.5, color: 0x00ffc3, transparent: true, opacity: 0.8 })
  const starsMesh = new THREE.Points(starsGeometry, starsMaterial)
  scene.add(starsMesh)

  // Pi Symbol Sphere (God-Chain Core)
  const sphereGeo = new THREE.SphereGeometry(8, 32, 32)
  const sphereMat = new THREE.MeshBasicMaterial({ color: 0x00ffc3, wireframe: true, transparent: true, opacity: 0.15 })
  const sphere = new THREE.Mesh(sphereGeo, sphereMat)
  scene.add(sphere)

  camera.position.z = 35

  const animate = () => {
    requestAnimationFrame(animate)
    starsMesh.rotation.y += 0.0005
    starsMesh.rotation.x += 0.0002
    sphere.rotation.y += 0.005
    sphere.rotation.x += 0.002
    renderer.render(scene, camera)
  }
  animate()

  // GSAP ENTRANCE
  gsap.from('.hero h1', { y: 100, opacity: 0, duration: 1.5, ease: 'power4.out' })
  gsap.from('.coords', { y: 30, opacity: 0, duration: 1, delay: 0.5 })
  gsap.from('.dual-box', { scale: 0.8, opacity: 0, duration: 1, delay: 0.8, ease: 'back.out(1.7)' })
  gsap.from('.card', { y: 50, opacity: 0, duration: 0.8, delay: 1, stagger: 0.15 })

  // Fake market price animation (nanti ganti API real)
  let price = 0.45
  setInterval(() => {
    price += (Math.random()-0.5)*0.02
    document.getElementById('marketPrice').innerText = `$${price.toFixed(4)}`
  }, 1500)

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
  })
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

#godchain-portal { font-family: 'Space Grotesk', sans-serif; background: #040508; color: #e0fffa; min-height: 100vh; position: relative; overflow-x: hidden; }
#cosmic-canvas { position: fixed; top:0; left:0; width:100%; height:100%; z-index:0; }
.overlay { position: relative; z-index:1; }

.hero { text-align: center; padding: 80px 20px 40px; }
.badge { display: inline-block; background: rgba(0,255,195,0.1); border: 1px solid #00ffc3; padding: 6px 14px; border-radius: 20px; font-size: 11px; letter-spacing: 2px; margin-bottom: 25px; color: #00ffc3; }
.hero h1 { font-size: clamp(36px, 8vw, 68px); line-height: 0.9; font-weight: 700; color: #00ffc3; text-shadow: 0 0 30px rgba(0,255,195,0.5); }
.hero h1 span { color: #fff; }
.coords { margin-top: 15px; opacity: 0.7; font-size: 14px; letter-spacing: 1px; }
.dual-box { display:flex; max-width: 520px; margin: 35px auto; background: rgba(10,20,25,0.8); backdrop-filter: blur(20px); border: 1px solid rgba(0,255,195,0.3); border-radius: 20px; padding: 20px; justify-content: space-around; }
.dual-item { display:flex; flex-direction:column; }
.label { font-size:10px; letter-spacing:2px; opacity:0.6; }
.value { font-size:22px; font-weight:700; margin-top:4px; }
.gcv.value { color:#00ffc3; }
.divider { width:1px; background: rgba(0,255,195,0.2); }

.content { max-width: 900px; margin: 0 auto; padding: 20px; }
.card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px; margin-bottom: 16px; backdrop-filter: blur(10px); }
.genesis { border-color: rgba(0,255,195,0.4); }
.card h3,.card h4 { color: #00ffc3; margin:0 0 6px; }
.status { margin-top:10px; font-size:12px; display:flex; align-items:center; gap:8px; }
.dot { width:8px; height:8px; background:#00ffc3; border-radius:50%; box-shadow:0 0 10px #00ffc3; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }

footer { text-align:center; padding: 50px 20px; opacity:0.5; font-size:12px; }
.small { font-size:10px; margin-top:6px; }
</style>
