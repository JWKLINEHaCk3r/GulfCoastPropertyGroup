<template>
  <div class="bg-black text-white min-h-screen overflow-hidden font-sans">
    <!-- Animated Background -->
    <div class="fixed inset-0 z-0">
      <canvas ref="canvas" class="w-full h-full"></canvas>
      <div class="absolute inset-0 bg-gradient-to-br from-blue-950/20 via-black to-cyan-950/20"></div>
    </div>

    <!-- Content Wrapper -->
    <div class="relative z-10">
      <!-- Premium Navigation -->
      <nav class="fixed top-0 w-full bg-black/40 backdrop-blur-xl border-b border-blue-500/10 z-50">
        <div class="max-w-7xl mx-auto px-6 py-5 flex justify-between items-center">
          <div class="flex items-center gap-4 group">
            <div class="w-14 h-14 rounded-xl overflow-hidden bg-gradient-to-br from-blue-500/20 to-cyan-500/20 flex items-center justify-center border border-cyan-500/30 group-hover:border-cyan-400/60 transition-all duration-300 shadow-lg shadow-cyan-500/10">
              <img src="@/assets/keystone-logo.svg" alt="Keystone" class="w-10 h-10 object-cover" />
            </div>
            <div>
              <h1 class="text-lg font-black bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 via-blue-300 to-cyan-400">KEYSTONE</h1>
              <p class="text-xs text-cyan-400/70 font-medium">VELOCITY CAPITAL</p>
            </div>
          </div>
          
          <div class="flex gap-12 items-center">
            <a href="#agents" class="text-sm font-medium text-gray-400 hover:text-cyan-300 transition duration-300">AI Agents</a>
            <a href="#automation" class="text-sm font-medium text-gray-400 hover:text-cyan-300 transition duration-300">Automation</a>
            <a href="#performance" class="text-sm font-medium text-gray-400 hover:text-cyan-300 transition duration-300">Performance</a>
            <button @click="scrollToSection('contact')" class="px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg font-semibold text-sm hover:shadow-xl hover:shadow-cyan-500/40 transition-all duration-300 transform hover:scale-105">
              Launch Platform
            </button>
          </div>
        </div>
      </nav>

      <!-- Hero Section - Premium 4K -->
      <section class="pt-40 pb-32 px-6 relative overflow-hidden">
        <!-- Animated Orbs -->
        <div class="absolute top-20 left-10 w-72 h-72 bg-cyan-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div class="absolute bottom-0 right-20 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse" style="animation-delay: 2s;"></div>

        <div class="max-w-6xl mx-auto relative z-10">
          <!-- Logo Center with Glow -->
          <div class="flex justify-center mb-12">
            <div class="w-48 h-48 rounded-2xl overflow-hidden bg-gradient-to-br from-blue-600/30 to-cyan-600/30 p-1 border border-cyan-400/40 shadow-2xl shadow-cyan-500/20 transform hover:scale-110 transition-transform duration-500">
              <div class="w-full h-full bg-black rounded-xl overflow-hidden flex items-center justify-center">
                <img src="@/assets/keystone-logo.svg" alt="Keystone Velocity Capital" class="w-40 h-40 object-cover drop-shadow-2xl" />
              </div>
            </div>
          </div>

          <!-- Main Headline -->
          <div class="text-center mb-8">
            <h2 class="text-7xl md:text-8xl font-black mb-6 leading-tight max-w-4xl mx-auto">
              <span class="block mb-4">CAPITAL</span>
              <span class="bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 via-blue-300 to-cyan-400 animate-pulse">AT</span>
              <span class="block">VELOCITY</span>
            </h2>
            
            <p class="text-xl md:text-2xl text-cyan-100/80 font-light max-w-3xl mx-auto mb-12 leading-relaxed">
              Enterprise-Grade AI Automation Platform powered by 12 specialized agents. 
              <span class="text-cyan-300 font-semibold">Scale your business to 6-7 figures effortlessly.</span>
            </p>
          </div>

          <!-- Key Metrics -->
          <div class="grid grid-cols-3 gap-6 max-w-2xl mx-auto mb-16">
            <div class="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-400/30 rounded-xl p-6 text-center hover:border-cyan-300/60 transition-all duration-300 group">
              <div class="text-4xl font-black text-cyan-300 group-hover:text-cyan-200 transition mb-2">100%</div>
              <div class="text-sm text-gray-400 font-medium">Automation</div>
            </div>
            <div class="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-400/30 rounded-xl p-6 text-center hover:border-cyan-300/60 transition-all duration-300 group">
              <div class="text-4xl font-black text-cyan-300 group-hover:text-cyan-200 transition mb-2">24/7</div>
              <div class="text-sm text-gray-400 font-medium">AI Agents Active</div>
            </div>
            <div class="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-400/30 rounded-xl p-6 text-center hover:border-cyan-300/60 transition-all duration-300 group">
              <div class="text-4xl font-black text-cyan-300 group-hover:text-cyan-200 transition mb-2">$$$</div>
              <div class="text-sm text-gray-400 font-medium">Revenue Growth</div>
            </div>
          </div>

          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row gap-6 justify-center">
            <button class="px-10 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl font-bold text-lg hover:shadow-2xl hover:shadow-cyan-500/50 transition-all duration-300 transform hover:scale-105 group relative overflow-hidden">
              <span class="relative z-10">Activate AI Agents</span>
              <div class="absolute inset-0 bg-gradient-to-r from-cyan-600 to-blue-700 rounded-xl scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left"></div>
            </button>
            <button class="px-10 py-4 border-2 border-cyan-400/50 rounded-xl font-bold text-lg hover:bg-cyan-400/10 transition-all duration-300 group">
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 to-blue-300 group-hover:from-cyan-200 group-hover:to-blue-200">View Demo</span>
            </button>
          </div>
        </div>
      </section>

      <!-- AI Agents Section -->
      <section id="agents" class="py-32 px-6 relative">
        <div class="max-w-7xl mx-auto">
          <div class="text-center mb-20">
            <h3 class="text-5xl md:text-6xl font-black mb-6">
              <span class="bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 to-blue-400">12 AI Agents</span>
              <br />Working For You
            </h3>
            <p class="text-lg text-gray-400 max-w-2xl mx-auto">Specialized autonomous agents, each expert in their domain. Working 24/7 to identify opportunities and execute deals.</p>
          </div>

          <!-- Agent Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="agent in agents" :key="agent.id" class="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-400/30 rounded-2xl p-8 hover:border-cyan-300/70 hover:shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300 group cursor-pointer">
              <div class="text-5xl mb-4 group-hover:scale-110 transition-transform duration-300">{{ agent.icon }}</div>
              <h4 class="text-xl font-black text-cyan-300 mb-3 group-hover:text-cyan-200">{{ agent.name }}</h4>
              <p class="text-gray-400 text-sm leading-relaxed">{{ agent.description }}</p>
              <div class="mt-6 h-1 w-0 group-hover:w-full bg-gradient-to-r from-cyan-500 to-blue-600 transition-all duration-300"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- Automation Flow Section -->
      <section id="automation" class="py-32 px-6 relative">
        <div class="max-w-7xl mx-auto">
          <h3 class="text-5xl md:text-6xl font-black text-center mb-20">
            <span class="bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 to-blue-400">Automated Workflow</span>
          </h3>

          <!-- Process Flow -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div v-for="(step, idx) in automationSteps" :key="idx" class="relative">
              <div class="bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-400/40 rounded-2xl p-8 h-full hover:border-cyan-300/70 transition-all duration-300 group">
                <div class="absolute -top-6 -left-6 w-12 h-12 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full flex items-center justify-center font-bold text-lg shadow-lg">
                  {{ idx + 1 }}
                </div>
                <h4 class="text-xl font-black text-cyan-300 mb-4 mt-4">{{ step.title }}</h4>
                <p class="text-gray-400 text-sm leading-relaxed">{{ step.description }}</p>
              </div>
              <div v-if="idx < automationSteps.length - 1" class="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                <svg class="w-8 h-8 text-cyan-500/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Performance Metrics -->
      <section id="performance" class="py-32 px-6 relative">
        <div class="max-w-7xl mx-auto">
          <h3 class="text-5xl md:text-6xl font-black text-center mb-20">
            <span class="bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 to-blue-400">Performance Analytics</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-400/30 rounded-2xl p-8">
              <h4 class="text-2xl font-black text-cyan-300 mb-6">Deal Pipeline</h4>
              <div class="space-y-4">
                <div v-for="metric in pipelineMetrics" :key="metric.label" class="flex items-center justify-between">
                  <span class="text-gray-400">{{ metric.label }}</span>
                  <div class="flex items-center gap-4">
                    <div class="w-32 h-2 bg-gray-800 rounded-full overflow-hidden">
                      <div class="h-full bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full" :style="{ width: metric.value + '%' }"></div>
                    </div>
                    <span class="text-cyan-300 font-bold text-sm w-12 text-right">{{ metric.value }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-400/30 rounded-2xl p-8">
              <h4 class="text-2xl font-black text-cyan-300 mb-6">Revenue Impact</h4>
              <div class="space-y-5">
                <div v-for="roi in revenueMetrics" :key="roi.label" class="border-b border-cyan-500/20 pb-4">
                  <p class="text-gray-400 text-sm mb-2">{{ roi.label }}</p>
                  <p class="text-3xl font-black text-cyan-400">{{ roi.value }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Features Showcase -->
      <section class="py-32 px-6 relative">
        <div class="max-w-7xl mx-auto">
          <h3 class="text-5xl md:text-6xl font-black text-center mb-20">
            <span class="bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 to-blue-400">Enterprise Features</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div v-for="feature in features" :key="feature.title" class="bg-gradient-to-br from-cyan-500/10 to-blue-500/10 border border-cyan-400/30 rounded-2xl p-8 hover:border-cyan-300/70 transition-all duration-300 group">
              <div class="text-5xl mb-4 group-hover:scale-110 transition-transform duration-300">{{ feature.icon }}</div>
              <h4 class="text-xl font-black text-cyan-300 mb-3 group-hover:text-cyan-200 transition">{{ feature.title }}</h4>
              <p class="text-gray-400 text-sm leading-relaxed">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Section -->
      <section id="contact" class="py-32 px-6 relative">
        <div class="max-w-4xl mx-auto text-center">
          <h3 class="text-6xl md:text-7xl font-black mb-8">
            Ready to Scale to
            <br />
            <span class="bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 to-blue-400">7 Figures?</span>
          </h3>
          
          <p class="text-xl text-gray-400 mb-12 max-w-2xl mx-auto">
            Join industry leaders already using Keystone Velocity Capital to automate their entire business and scale exponentially.
          </p>

          <div class="flex flex-col sm:flex-row gap-6 justify-center">
            <button class="px-12 py-5 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl font-bold text-lg hover:shadow-2xl hover:shadow-cyan-500/50 transition-all duration-300 transform hover:scale-105">
              Get Started Now
            </button>
            <button class="px-12 py-5 border-2 border-cyan-400/50 rounded-xl font-bold text-lg hover:bg-cyan-400/10 transition-all duration-300">
              Schedule Demo
            </button>
          </div>
        </div>
      </section>

      <!-- Footer -->
      <footer class="border-t border-cyan-500/10 py-12 px-6">
        <div class="max-w-7xl mx-auto text-center text-gray-500 text-sm">
          <p>&copy; 2026 Keystone Velocity Capital. Enterprise AI Automation Platform.</p>
          <p class="mt-4">Powering the next generation of real estate entrepreneurs.</p>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
const hoveredAgent = ref(null)

const agents = ref([
  { id: 1, name: 'Lead Scout', icon: '🔍', description: 'Finds motivated sellers across 50+ states' },
  { id: 2, name: 'Offer Generator', icon: '💰', description: 'AI-calculated optimal offers in real-time' },
  { id: 3, name: 'Buyer Matcher', icon: '👥', description: 'Matches deals with perfect buyer profiles' },
  { id: 4, name: 'Contract Agent', icon: '📝', description: 'Generates state-specific legal contracts' },
  { id: 5, name: 'Negotiation Bot', icon: '🤝', description: 'Automates seller communications' },
  { id: 6, name: 'SEO Optimizer', icon: '🔗', description: 'Builds organic lead generation channels' },
  { id: 7, name: 'Data Analyst', icon: '📊', description: 'Real-time market analysis and comps' },
  { id: 8, name: 'Finance Agent', icon: '🏦', description: 'Connects with hard money lenders' },
  { id: 9, name: 'Legal Advisor', icon: '⚖️', description: 'Compliance and contract review' },
  { id: 10, name: 'CRM Master', icon: '📱', description: 'Manages 1000s of leads automatically' },
  { id: 11, name: 'Closer Agent', icon: '✅', description: 'Guides deals to closing' },
  { id: 12, name: 'Exit Strategist', icon: '🚀', description: 'Maximizes profit per transaction' }
])

const automationSteps = [
  { title: 'DISCOVER', description: 'AI agents scan millions of properties for investment opportunities' },
  { title: 'ANALYZE', description: 'Instant market analysis, comps, and deal scoring' },
  { title: 'EXECUTE', description: 'Automated offers, contracts, and buyer matching' },
  { title: 'CLOSE', description: '24/7 deal management until closing' }
]

const pipelineMetrics = [
  { label: 'Leads Processed', value: 98 },
  { label: 'Offers Accepted', value: 87 },
  { label: 'Deals Closed', value: 76 },
  { label: 'Success Rate', value: 92 }
]

const revenueMetrics = [
  { label: 'Avg Deal Size', value: '+$45K' },
  { label: 'Monthly Volume', value: '180+ Deals' },
  { label: 'Time to Close', value: '8-10 Days' },
  { label: 'ROI Multiple', value: '12x Return' }
]

const features = [
  { title: 'AI Agent Network', description: '12 specialized agents working in harmony', icon: '🤖' },
  { title: '24/7 Automation', description: 'Your business never sleeps, neither do we', icon: '⚡' },
  { title: 'Real-Time Analytics', description: 'Live dashboards and instant insights', icon: '📊' },
  { title: 'Multi-Channel Sourcing', description: 'Leads from 50+ states and platforms', icon: '🌍' },
  { title: 'Smart Matching', description: 'Perfect deal-to-buyer matching at scale', icon: '🎯' },
  { title: 'Enterprise Security', description: 'Bank-level encryption and compliance', icon: '🔒' }
]

// Animated Background Canvas
const initCanvas = () => {
  if (!canvas.value) return

  const ctx = canvas.value.getContext('2d')
  canvas.value.width = window.innerWidth
  canvas.value.height = window.innerHeight

  const particles = []
  const particleCount = 50

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.value.width,
      y: Math.random() * canvas.value.height,
      radius: Math.random() * 2,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      opacity: Math.random() * 0.5 + 0.2
    })
  }

  const animate = () => {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.02)'
    ctx.fillRect(0, 0, canvas.value.width, canvas.value.height)

    particles.forEach((p, idx) => {
      p.x += p.vx
      p.y += p.vy

      if (p.x < 0) p.x = canvas.value.width
      if (p.x > canvas.value.width) p.x = 0
      if (p.y < 0) p.y = canvas.value.height
      if (p.y > canvas.value.height) p.y = 0

      ctx.fillStyle = `rgba(34, 211, 238, ${p.opacity})`
      ctx.beginPath()
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2)
      ctx.fill()

      particles.forEach((p2, idx2) => {
        if (idx < idx2) {
          const dx = p.x - p2.x
          const dy = p.y - p2.y
          const distance = Math.sqrt(dx * dx + dy * dy)

          if (distance < 150) {
            ctx.strokeStyle = `rgba(34, 211, 238, ${(1 - distance / 150) * 0.2})`
            ctx.lineWidth = 0.5
            ctx.beginPath()
            ctx.moveTo(p.x, p.y)
            ctx.lineTo(p2.x, p2.y)
            ctx.stroke()
          }
        }
      })
    })

    requestAnimationFrame(animate)
  }

  animate()
}

const handleWindowResize = () => {
  if (canvas.value) {
    canvas.value.width = window.innerWidth
    canvas.value.height = window.innerHeight
  }
}

const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  element?.scrollIntoView({ behavior: 'smooth' })
}

onMounted(() => {
  initCanvas()
  window.addEventListener('resize', handleWindowResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleWindowResize)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

canvas {
  display: block;
}

@keyframes pulse-slow {
  0%, 100% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
}

.animate-pulse {
  animation: pulse-slow 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

::selection {
  background: rgba(34, 211, 238, 0.3);
  color: #e0f2fe;
}
</style>
</template>
