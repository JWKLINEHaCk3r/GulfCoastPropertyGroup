import { createApp } from 'vue'
import Landing from './pages/Landing.vue'

// Initialize Sentry if configured
if (import.meta.env.VITE_SENTRY_DSN) {
	// dynamic import to avoid adding dependency unless configured
	import('@sentry/browser').then((Sentry) => {
		Sentry.init({ dsn: import.meta.env.VITE_SENTRY_DSN })
	}).catch(() => {})
}

const app = createApp(Landing)
app.mount('#app')
