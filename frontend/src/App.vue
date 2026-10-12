<template>
  <div id="godchain-portal">
    <canvas ref="canvasRef" id="cosmic-canvas"></canvas>

    <div class="overlay">
      <header class="hero">
        <div class="badge">🌍 LIVE ON VERCEL • <span :class="{live: isLive}">● {{ isLive? 'LIVE PRICE' : 'CONNECTING' }}</span></div>
        <h1 class="glitch" data-text="Cijoho Genesis">Cijoho Genesis<br><span>God-Chain</span></h1>
        <p class="coords">
          ID 314159 | Ti Cijoho Pikeun Dunia |
          <a href="https://www.google.com/maps/search/?api=1&query=-6.979,108.484" target="_blank" class="coord-link">-6.979,108.484 📍</a>
        </p>

        <div class="dual-box">
          <div class="dual-item gcv">
            <span class="label">SYMBOLIC GCV</span>
            <span class="value">$314,159</span>
            <span class="sub">Community Consensus</span>
          </div>
          <div class="divider"></div>
          <div class="dual-item market">
            <span class="label">MARKET PRICE <span v-if="isLive" class="dot-live"></span></span>
            <span class="value">${{ marketPrice.toFixed(4) }}</span>
            <span class="sub">{{ change24h > 0? '+' : '' }}{{ change24h.toFixed(2) }}% 24h • OKX</span>
          </div>
        </div>
        <p class="dual-note">PiDualTx = GCV for Warung, Market for Exchange. Cijoho controls both.</p>
      </header>

      <main class="content">
        <div class="card genesis" @click="openMaps">
          <h3>🏛️ Warung Pi #0</h3>
          <p>Capital of Civilization — Genesis Block of Cijoho</p>
          <div class="status">
            <span class="dot"></span> God-Chain Active — Click to Navigate
          </div>
          <div class="tap-hint">👆 Tap sphere to mint • Tap card to navigate</div>
        </div>

        <div class="grid">
          <div class="card">
            <h4>PiDualTx System</h4>
            <p>Dual Value Consensus Engine<br><b>{{ piAmount }} Pi = ${{ (piAmount * marketPrice).toFixed(2) }} market / ${{ (piAmount*314159).toLocaleString() }} GCV</b></p>
          </div>
          <div class="card">
            <h4>Stellar SDK</h4>
            <p>Connected to Pi Network<br><span class="mono">ID: 314159 • Block #0 Cijoho</span></p>
          </div>
        </div>

        <router-view />
      </main>

      <footer>
        <p>© 2026 Cijoho Genesis | KOSASIH - Bapak Peradaban Cijoho</p>
        <p class="small">No Official Pi Price - Community Consensus Value. Market: ${{ marketPrice.toFixed(4) }} Live</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, onUnmounted } from 'vue'
import * as THREE from 'three'
import gsap from 'gsap'

const canvasRef = ref(null)
const marketPrice = ref(0.08251)
const change24h = ref(-1.06)
const isLive = ref(false)
const piAmount = ref(1)

function openMaps(){
  window.open('https://www.google.com/maps/search/?api=1&query=-6.979,108.484','_blank')
}

async function fetchPiPrice(){
  try{
    const r = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=pi-network&vs_currencies=usd&include_24hr_change=true')
    const j = await r.json()
    if(j['pi-network']?.usd){
      marketPrice.value = j['pi-network'].usd
      change24h.value = j['pi-network'].usd_24h_change || change24h.value
      isLive.value = true
    }
  }catch(e){
    // fallback tetap live price dari OKX tadi: 0.08251
    const r2 = await fetch('https://api.okx.com/api/v5/market/ticker?instId=PI-USDT').then(x=>x.json()).catch(()=>null)
    if(r2?.data?.[0]?.last){ marketPrice.value = parseFloat(r2.data[0].last); isLive.value=true }
  }
}

onMounted(() => {
  fetchPiPrice()
  const interval = setInterval(fetchPiPrice, 30000)

  const scene = new THREE.Scene()
  const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  const renderer = new THREE.WebGLRenderer({ canvas: canvasRef.value, alpha: true, antialias: true })
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,2))

  // Stars
  const starsGeometry = new THREE.BufferGeometry()
  const starsCount = 3000
  const posArray = new Float32Array(starsCount * 3)
  for(let i=0;i<starsCount*3;i++) posArray[i] = (Math.random()-0.5)*2000
  starsGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3))
  const starsMaterial = new THREE.PointsMaterial({ size: 1.4, color: 0x00ffc3, transparent: true, opacity: 0.8, sizeAttenuation: true })
  const starsMesh = new THREE.Points(starsGeometry, starsMaterial)
  scene.add(starsMesh)

  // God-Chain Core Sphere
  const sphereGeo = new THREE.SphereGeometry(8, 32, 32)
  const sphereMat = new THREE.MeshBasicMaterial({ color: 0x00ffc3, wireframe: true, transparent: true, opacity: 0.18 })
  const sphere = new THREE.Mesh(sphereGeo, sphereMat)
  scene.add(sphere)
  const innerGeo = new THREE.SphereGeometry(3.5, 32, 32)
  const innerMat = new THREE.MeshBasicMaterial({ color: 0x00ffc3, transparent: true, opacity: 0.08 })
  const inner = new THREE.Mesh(innerGeo, innerMat)
  scene.add(inner)

  camera.position.z = 35

  // Drag to rotate
  let isDragging = false, prevX=0, prevY=0
  const onDown = (e)=>{ isDragging=true; prevX = e.touches?e.touches[0].clientX:e.clientX; prevY = e.touches?e.touches[0].clientY:e.clientY }
  const onUp = ()=>{ isDragging=false }
  const onMove = (e)=>{
    if(!isDragging) return
    const x = e.touches?e.touches[0].clientX:e.clientX
    const y = e.touches?e.touches[0].clientY:e.clientY
    sphere.rotation.y += (x-prevX)*0.01
    sphere.rotation.x += (y-prevY)*0.01
    prevX=x; prevY=y
  }
  window.addEventListener('mousedown', onDown); window.addEventListener('mouseup', onUp); window.addEventListener('mousemove', onMove)
  window.addEventListener('touchstart', onDown); window.addEventListener('touchend', onUp); window.addEventListener('touchmove', onMove)

  // Click sphere -> effect
  const raycaster = new THREE.Raycaster()
  const mouse = new THREE.Vector2()
  const onClick = (e)=>{
    mouse.x = (e.clientX/window.innerWidth)*2-1; mouse.y = -(e.clientY/window.innerHeight)*2+1
    raycaster.setFromCamera(mouse, camera)
    if(raycaster.intersectObject(sphere).length){
      gsap.to(sphere.scale, { x:1.3, y:1.3, z:1.3, duration:0.2, yoyo:true, repeat:1, ease:'power2.out' })
    }
  }
  window.addEventListener('click', onClick)

  const animate = () => {
    requestAnimationFrame(animate)
    if(!isDragging){ sphere.rotation.y += 0.005; sphere.rotation.x += 0.002 }
    inner.rotation.y -= 0.008
    starsMesh.rotation.y += 0.0005
    renderer.render(scene, camera)
  }
  animate()

  // GSAP ENTRANCE
  gsap.from('.hero h1', { y: 100, opacity: 0, duration: 1.5, ease: 'power4.out' })
  gsap.from('.coords', { y: 30, opacity: 0, duration: 1, delay: 0.5 })
  gsap.from('.dual-box', { scale: 0.8, opacity: 0, duration: 1, delay: 0.8, ease: 'back.out(1.7)' })
  gsap.from('.card', { y: 50, opacity: 0, duration: 0.8, delay: 1, stagger: 0.15 })

  const onResize = () => {
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize(window.innerWidth, window.innerHeight)
  }
  window.addEventListener('resize', onResize)

  onUnmounted(()=>{
    clearInterval(interval)
    window.removeEventListener('resize', onResize)
    window.removeEventListener('mousedown', onDown); window.removeEventListener('mouseup', onUp); window.removeEventListener('mousemove', onMove)
    window.removeEventListener('touchstart', onDown); window.removeEventListener('touchend', onUp); window.removeEventListener('touchmove', onMove)
    window.removeEventListener('click', onClick)
  })
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');
#godchain-portal { font-family: 'Space Grotesk', sans-serif; background: #040508; color: #e0fffa; min-height: 100vh; position: relative; overflow-x: hidden; }
#cosmic-canvas { position: fixed; top:0; left:0; width:100%; height:100%; z-index:0; cursor: grab; }
#cosmic-canvas:active{ cursor: grabbing; }
.overlay { position: relative; z-index:1; pointer-events: none; }
.overlay.hero,.overlay.content,.overlay footer { pointer-events: auto; }
.hero { text-align: center; padding: 80px 20px 40px; }
.badge { display: inline-block; background: rgba(0,255,195,0.1); border: 1px solid #00ffc3; padding: 6px 14px; border-radius: 20px; font-size: 11px; letter-spacing: 2px; margin-bottom: 25px; color: #00ffc3; }
.badge.live{ color:#ff3b3b; }.badge.live.live{ color:#00ffc3; }
.hero h1 { font-size: clamp(36px, 8vw, 68px); line-height: 0.9; font-weight: 700; color: #00ffc3; text-shadow: 0 0 30px rgba(0,255,195,0.5); }
.hero h1 span { color: #fff; }
.coords { margin-top: 15px; opacity: 0.7; font-size: 14px; letter-spacing: 1px; }
.coord-link{ color:#00ffc3; text-decoration:none; border-bottom:1px dashed #00ffc3; }
.dual-box { display:flex; max-width: 560px; margin: 35px auto 10px; background: rgba(10,20,25,0.85); backdrop-filter: blur(20px); border: 1px solid rgba(0,255,195,0.3); border-radius: 20px; padding: 20px; justify-content: space-around; }
.dual-item { display:flex; flex-direction:column; }
.label { font-size:10px; letter-spacing:2px; opacity:0.6; display:flex; align-items:center; gap:6px; }
.value { font-size:24px; font-weight:700; margin-top:4px; }
.sub{ font-size:10px; opacity:0.5; margin-top:4px; }
.divider { width:1px; background: rgba(0,255,195,0.2); }
.dual-note{ font-size:11px; opacity:0.5; margin-top:12px; }
.dot-live{ width:8px; height:8px; background:#00ff88; border-radius:50%; display:inline-block; box-shadow:0 0 8px #00ff88; animation: pulse 1.2s infinite; }
.content { max-width: 900px; margin: 0 auto; padding: 20px; }
.card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px; margin-bottom: 16px; backdrop-filter: blur(10px); cursor:pointer; transition:0.3s; }
.card:hover{ border-color: rgba(0,255,195,0.4); transform: translateY(-2px); }
.genesis { border-color: rgba(0,255,195,0.4); }
.card h3,.card h4 { color: #00ffc3; margin:0 0 6px; }
.status { margin-top:10px; font-size:12px; display:flex; align-items:center; gap:8px; }
.dot { width:8px; height:8px; background:#00ffc3; border-radius:50%; box-shadow:0 0 10px #00ffc3; animation: pulse 2s infinite; }
.tap-hint{ font-size:10px; opacity:0.4; margin-top:8px; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.mono{ font-family: monospace; font-size:11px; }
footer { text-align:center; padding: 50px 20px; opacity:0.5; font-size:12px; }
.small { font-size:10px; margin-top:6px; }
</style>
