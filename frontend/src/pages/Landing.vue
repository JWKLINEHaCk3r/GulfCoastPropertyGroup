<template>
  <div class="bg-black text-white min-h-screen overflow-hidden">
    <!-- Navigation Bar -->
    <nav class="fixed top-0 w-full bg-black/80 backdrop-blur z-50 border-b border-blue-500/20">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded overflow-hidden bg-white/5 flex items-center justify-center">
            <img v-if="!logoError" :src="logoPath" alt="logo" class="w-full h-full object-cover" @error="logoError = true" />
            <span v-else class="font-bold text-black">GC</span>
          </div>
          <h1 class="text-sm font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
            Gulf Coast Property Group
          </h1>
        </div>
        
        <div class="flex gap-8 items-center">
          <a href="#features" class="text-sm hover:text-cyan-400 transition">Features</a>
          <a href="#pricing" class="text-sm hover:text-cyan-400 transition">Pricing</a>
          <a href="#contact" class="text-sm hover:text-cyan-400 transition">Contact</a>
          <button @click="isLoginOpen = true" class="px-4 py-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded text-sm font-medium hover:shadow-lg hover:shadow-cyan-500/50 transition">
            Sign In
          </button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-32 pb-20 px-4 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-b from-blue-500/10 to-transparent pointer-events-none"></div>
      <div class="max-w-5xl mx-auto relative z-10 text-center">
        <h2 class="text-5xl md:text-7xl font-bold mb-6 leading-tight">
          Find <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-teal-400">Every Deal</span> in America
        </h2>
        <p class="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
          AI-powered real estate automation that finds motivated sellers, generates offers, and closes deals 24/7. Find 100+ deals daily. Close them in 10 days or less.
        </p>
        
        <div class="flex gap-4 justify-center mb-12">
          <button @click="isSignupOpen = true" class="px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg font-semibold hover:shadow-lg hover:shadow-cyan-500/50 transition text-lg">
            Start Free Trial
          </button>
          <button class="px-8 py-4 border border-cyan-400/50 rounded-lg font-semibold hover:bg-cyan-400/10 transition text-lg">
            Book Demo
          </button>
        </div>

        <div class="grid grid-cols-3 gap-8 max-w-3xl mx-auto text-sm">
          <div class="border border-blue-500/30 rounded p-4 bg-blue-500/5">
            <div class="text-2xl font-bold text-cyan-400">100+</div>
            <div class="text-gray-400">Daily Leads</div>
          </div>
          <div class="border border-blue-500/30 rounded p-4 bg-blue-500/5">
            <div class="text-2xl font-bold text-cyan-400">10x</div>
            <div class="text-gray-400">Faster Sourcing</div>
          </div>
          <div class="border border-blue-500/30 rounded p-4 bg-blue-500/5">
            <div class="text-2xl font-bold text-cyan-400">50+</div>
            <div class="text-gray-400">States Coverage</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Value Propositions -->
    <section class="py-20 px-4 border-t border-blue-500/20">
      <div class="max-w-6xl mx-auto">
        <h3 class="text-3xl font-bold mb-12 text-center">Solve Every Problem in Real Estate</h3>
        
        <div class="grid md:grid-cols-5 gap-4">
          <div class="border border-blue-500/30 rounded p-6 bg-blue-500/5 hover:border-cyan-400/50 transition">
            <div class="text-3xl mb-4">🔎</div>
            <h4 class="font-bold mb-2 text-cyan-400">Find Deals</h4>
            <p class="text-sm text-gray-400">Scan 50+ states for FSBO, tax delinquent, distressed properties daily</p>
          </div>
          
          <div class="border border-blue-500/30 rounded p-6 bg-blue-500/5 hover:border-cyan-400/50 transition">
            <div class="text-3xl mb-4">💰</div>
            <h4 class="font-bold mb-2 text-cyan-400">Smart Offers</h4>
            <p class="text-sm text-gray-400">AI calculates optimal offers using market data, comps, and cash flow analysis</p>
          </div>
          
          <div class="border border-blue-500/30 rounded p-6 bg-blue-500/5 hover:border-cyan-400/50 transition">
            <div class="text-3xl mb-4">👥</div>
            <h4 class="font-bold mb-2 text-cyan-400">Match Buyers</h4>
            <p class="text-sm text-gray-400">Auto-match deals with investors who want exactly what you have</p>
          </div>
          
          <div class="border border-blue-500/30 rounded p-6 bg-blue-500/5 hover:border-cyan-400/50 transition">
            <div class="text-3xl mb-4">📝</div>
            <h4 class="font-bold mb-2 text-cyan-400">Sign Contracts</h4>
            <p class="text-sm text-gray-400">Generate state-specific contracts and get e-signatures in minutes</p>
          </div>
          
          <div class="border border-blue-500/30 rounded p-6 bg-blue-500/5 hover:border-cyan-400/50 transition">
            <div class="text-3xl mb-4">🏦</div>
            <h4 class="font-bold mb-2 text-cyan-400">Secure Funding</h4>
            <p class="text-sm text-gray-400">Match with hard money lenders and get pre-approval instantly</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="py-20 px-4 border-t border-blue-500/20">
      <div class="max-w-4xl mx-auto">
        <h3 class="text-3xl font-bold mb-12 text-center">Watch the Automation Do the Work</h3>
        
        <div class="space-y-6">
          <div class="flex gap-6 items-start">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center flex-shrink-0">
              <span class="font-bold">1</span>
            </div>
            <div>
              <h4 class="font-bold text-lg mb-2">AI Finds 100+ Daily Leads</h4>
              <p class="text-gray-400">Our agents scan millions of properties daily across all 50 states and score each by motivation level</p>
            </div>
          </div>
          
          <div class="flex gap-6 items-start">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center flex-shrink-0">
              <span class="font-bold">2</span>
            </div>
            <div>
              <h4 class="font-bold text-lg mb-2">Automated Outreach & Qualification</h4>
              <p class="text-gray-400">SMS + Email follow-ups with personalized messages. System auto-qualifies which sellers want to sell</p>
            </div>
          </div>
          
          <div class="flex gap-6 items-start">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center flex-shrink-0">
              <span class="font-bold">3</span>
            </div>
            <div>
              <h4 class="font-bold text-lg mb-2">Generate Smart Offers</h4>
              <p class="text-gray-400">AI calculates ARV, repair costs, and optimal price. Send offers automatically via email</p>
            </div>
          </div>
          
          <div class="flex gap-6 items-start">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center flex-shrink-0">
              <span class="font-bold">4</span>
            </div>
            <div>
              <h4 class="font-bold text-lg mb-2">Negotiate & Get Signature</h4>
              <p class="text-gray-400">System handles counter-offers, generates contracts, and sends for esignature. You just review & approve</p>
            </div>
          </div>
          
          <div class="flex gap-6 items-start">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center flex-shrink-0">
              <span class="font-bold">5</span>
            </div>
            <div>
              <h4 class="font-bold text-lg mb-2">Match with Buyer & Close</h4>
              <p class="text-gray-400">System shows deal to investors who want it, coordinates due diligence, gets buyer into position for closing</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Results Section -->
    <section class="py-20 px-4 border-t border-blue-500/20">
      <div class="max-w-5xl mx-auto">
        <h3 class="text-3xl font-bold mb-12 text-center">Results That Don't Lie</h3>
        
        <div class="grid md:grid-cols-3 gap-8">
          <div class="p-8 border border-blue-500/30 rounded bg-gradient-to-br from-blue-500/10 to-transparent">
            <div class="text-4xl font-bold text-cyan-400 mb-2">312%</div>
            <p class="text-gray-400 text-sm">Average ROI increase in first quarter (more deals at better prices)</p>
          </div>
          
          <div class="p-8 border border-blue-500/30 rounded bg-gradient-to-br from-blue-500/10 to-transparent">
            <div class="text-4xl font-bold text-cyan-400 mb-2">10x</div>
            <p class="text-gray-400 text-sm">More leads generated compared to manual methods (per month)</p>
          </div>
          
          <div class="p-8 border border-blue-500/30 rounded bg-gradient-to-br from-blue-500/10 to-transparent">
            <div class="text-4xl font-bold text-cyan-400 mb-2">5 min</div>
            <p class="text-gray-400 text-sm">Average time to send offer (vs. hours of manual research)</p>
          </div>

          <div class="p-8 border border-blue-500/30 rounded bg-gradient-to-br from-blue-500/10 to-transparent">
            <div class="text-4xl font-bold text-cyan-400 mb-2">50+</div>
            <p class="text-gray-400 text-sm">Statewide coverage (all 50 states + major metros)</p>
          </div>
          
          <div class="p-8 border border-blue-500/30 rounded bg-gradient-to-br from-blue-500/10 to-transparent">
            <div class="text-4xl font-bold text-cyan-400 mb-2">1000+</div>
            <p class="text-gray-400 text-sm">Properties analyzed daily for your target market</p>
          </div>
          
          <div class="p-8 border border-blue-500/30 rounded bg-gradient-to-br from-blue-500/10 to-transparent">
            <div class="text-4xl font-bold text-cyan-400 mb-2">99.9%</div>
            <p class="text-gray-400 text-sm">System uptime (deals running 24/7 while you sleep)</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section class="py-20 px-4 border-t border-blue-500/20" id="pricing">
      <div class="max-w-6xl mx-auto">
        <h3 class="text-3xl font-bold mb-4 text-center">Simple, Transparent Pricing</h3>
        <p class="text-center text-gray-400 mb-12">No hidden fees. Pay for what you use. Cancel anytime.</p>
        
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Starter Plan -->
          <div class="border border-blue-500/30 rounded-lg p-8 bg-blue-500/5 hover:border-cyan-400/50 transition">
            <div class="text-2xl font-bold mb-2">Starter</div>
            <div class="text-4xl font-bold text-cyan-400 mb-1">$299<span class="text-lg text-gray-400">/mo</span></div>
            <p class="text-sm text-gray-400 mb-8">For wholesalers getting started</p>
            
            <ul class="space-y-4 text-sm mb-8">
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> 30 leads/day</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Automated outreach</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Offer generation</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Basic analytics</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Email & SMS</li>
              <li class="flex gap-3"><span class="text-gray-600">✗</span> Contract signing</li>
            </ul>
            
            <button class="w-full py-2 border border-blue-400 rounded hover:bg-blue-400/10 transition">
              Get Started
            </button>
          </div>

          <!-- Professional Plan (Popular) -->
          <div class="border border-cyan-400/50 rounded-lg p-8 bg-gradient-to-br from-cyan-500/10 to-blue-500/5 hover:border-cyan-400 transition relative">
            <div class="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gradient-to-r from-blue-500 to-cyan-500 px-4 py-1 rounded-full text-sm font-semibold">
              MOST POPULAR
            </div>
            
            <div class="text-2xl font-bold mb-2">Professional</div>
            <div class="text-4xl font-bold text-cyan-400 mb-1">$799<span class="text-lg text-gray-400">/mo</span></div>
            <p class="text-sm text-gray-400 mb-8">For serious wholesalers</p>
            
            <ul class="space-y-4 text-sm mb-8">
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> 100+ leads/day</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Automated outreach</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Smart offer generation</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Advanced analytics</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Contract signing</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Investor matching</li>
            </ul>
            
            <button class="w-full py-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded hover:shadow-lg hover:shadow-cyan-500/50 transition font-semibold">
              Start Free Trial
            </button>
          </div>

          <!-- Enterprise Plan -->
          <div class="border border-blue-500/30 rounded-lg p-8 bg-blue-500/5 hover:border-cyan-400/50 transition">
            <div class="text-2xl font-bold mb-2">Enterprise</div>
            <div class="text-4xl font-bold text-cyan-400 mb-1">Custom<span class="text-lg text-gray-400">pricing</span></div>
            <p class="text-sm text-gray-400 mb-8">For teams & large operations</p>
            
            <ul class="space-y-4 text-sm mb-8">
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Unlimited leads</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Everything in Pro</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Private white-label option</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Dedicated account manager</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> Custom integrations</li>
              <li class="flex gap-3"><span class="text-cyan-400">✓</span> API access</li>
            </ul>
            
            <button class="w-full py-2 border border-blue-400 rounded hover:bg-blue-400/10 transition">
              Book Demo
            </button>
          </div>
        </div>

        <div class="mt-12 grid md:grid-cols-2 gap-8 max-w-3xl mx-auto">
          <div class="border border-blue-500/30 rounded p-6 bg-blue-500/5">
            <h4 class="font-bold mb-4">5 Revenue Streams Included</h4>
            <ul class="space-y-2 text-sm text-gray-400">
              <li>✓ Wholesale finder's fees (3-7%)</li>
              <li>✓ Investor subscriptions</li>
              <li>✓ Lead sales to partners</li>
              <li>✓ Market report sales</li>
              <li>✓ Affiliate commissions</li>
            </ul>
          </div>
          
          <div class="border border-blue-500/30 rounded p-6 bg-blue-500/5">
            <h4 class="font-bold mb-4">No Contracts. No Setup Fees.</h4>
            <ul class="space-y-2 text-sm text-gray-400">
              <li>✓ Cancel anytime</li>
              <li>✓ Money-back guarantee</li>
              <li>✓ Free onboarding</li>
              <li>✓ 24/7 support</li>
              <li>✓ Regular training</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section class="py-20 px-4 border-t border-blue-500/20">
      <div class="max-w-4xl mx-auto">
        <h3 class="text-3xl font-bold mb-12 text-center">Real Results from Real Users</h3>
        
        <div class="space-y-8">
          <div class="border border-blue-500/30 rounded p-8 bg-blue-500/5">
            <div class="flex gap-4">
              <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-cyan-400 flex-shrink-0"></div>
              <div class="flex-1">
                <h4 class="font-bold mb-1">James Mitchell</h4>
                <p class="text-sm text-gray-400 mb-4">Texas Wholesaler, 12+ years experience</p>
                <p class="text-gray-300 mb-4">"I was manually sourcing 10-15 leads per month. With Gulf Coast, I'm getting 100+ qualified leads daily. Closed 15 deals in my first quarter. Best investment for my business."</p>
                <div class="text-yellow-400">★★★★★</div>
              </div>
            </div>
          </div>

          <div class="border border-blue-500/30 rounded p-8 bg-blue-500/5">
            <div class="flex gap-4">
              <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-cyan-400 flex-shrink-0"></div>
              <div class="flex-1">
                <h4 class="font-bold mb-1">Sarah Chen</h4>
                <p class="text-sm text-gray-400 mb-4">Investor & Fund Manager</p>
                <p class="text-gray-300 mb-4">"The investor portal is legitimately game-changing. I have 50+ on-market deals at my fingertips. The automatic deal matching saved me 15+ hours per week searching."</p>
                <div class="text-yellow-400">★★★★★</div>
              </div>
            </div>
          </div>

          <div class="border border-blue-500/30 rounded p-8 bg-blue-500/5">
            <div class="flex gap-4">
              <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-cyan-400 flex-shrink-0"></div>
              <div class="flex-1">
                <h4 class="font-bold mb-1">Michael Rodriguez</h4>
                <p class="text-sm text-gray-400 mb-4">Hard Money Lender</p>
                <p class="text-gray-300 mb-4">"The API integration means I see qualified deals in real-time. This system is helping me deploy capital way faster. My portfolio ROI is up 40%."</p>
                <div class="text-yellow-400">★★★★★</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Final CTA -->
    <section class="py-20 px-4 border-t border-blue-500/20 bg-gradient-to-b from-transparent to-blue-500/10">
      <div class="max-w-4xl mx-auto text-center">
        <h3 class="text-4xl font-bold mb-6">Ready to Automate Your Business?</h3>
        <p class="text-xl text-gray-300 mb-8">Start finding deals and closing contracts in minutes, not months.</p>
        
        <div class="flex gap-4 justify-center">
          <button @click="isSignupOpen = true" class="px-8 py-4 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg font-semibold hover:shadow-lg hover:shadow-cyan-500/50 transition text-lg">
            Start Free 7-Day Trial
          </button>
          <button class="px-8 py-4 border border-cyan-400/50 rounded-lg font-semibold hover:bg-cyan-400/10 transition text-lg">
            Schedule Demo
          </button>
        </div>
        
        <p class="text-sm text-gray-400 mt-8">✓ No credit card required  ✓ Access to all features  ✓ 30-day money-back guarantee</p>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-blue-500/20 py-12 px-4">
      <div class="max-w-6xl mx-auto">
        <div class="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <h4 class="font-bold mb-4">Product</h4>
            <ul class="space-y-2 text-sm text-gray-400">
              <li><a href="#" class="hover:text-cyan-400">Features</a></li>
              <li><a href="#" class="hover:text-cyan-400">Pricing</a></li>
              <li><a href="#" class="hover:text-cyan-400">API Docs</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="font-bold mb-4">Company</h4>
            <ul class="space-y-2 text-sm text-gray-400">
              <li><a href="#" class="hover:text-cyan-400">About</a></li>
              <li><a href="#" class="hover:text-cyan-400">Blog</a></li>
              <li><a href="#" class="hover:text-cyan-400">Contact</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="font-bold mb-4">Legal</h4>
            <ul class="space-y-2 text-sm text-gray-400">
              <li><a href="#" class="hover:text-cyan-400">Privacy</a></li>
              <li><a href="#" class="hover:text-cyan-400">Terms</a></li>
              <li><a href="#" class="hover:text-cyan-400">Compliance</a></li>
            </ul>
          </div>
          
          <div>
            <h4 class="font-bold mb-4">Connect</h4>
            <ul class="space-y-2 text-sm text-gray-400">
              <li><a href="#" class="hover:text-cyan-400">Twitter</a></li>
              <li><a href="#" class="hover:text-cyan-400">LinkedIn</a></li>
              <li><a href="#" class="hover:text-cyan-400">Facebook</a></li>
            </ul>
          </div>
        </div>
        
        <div class="border-t border-blue-500/20 pt-8 flex justify-between items-center text-sm text-gray-400">
          <p>&copy; 2026 Gulf Coast Property Group. All rights reserved.</p>
          <p>Made with ❤️ for real estate wholesalers</p>
        </div>
      </div>
    </footer>

    <!-- Auth Modals will go here -->
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isLoginOpen = ref(false)
const isSignupOpen = ref(false)

// Runtime logo path; place your logo at `frontend/src/assets/logo.png` or
// set your build pipeline to copy an image to `/assets/logo.png`.
const logoPath = '/assets/logo.png'
const logoError = ref(false)
</script>

<style scoped>
/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}
</style>
