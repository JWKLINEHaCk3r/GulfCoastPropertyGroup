Netlify Functions for Gulf Coast Property Group

Files:
- `utils.js` - small helper functions for JSON response and body parsing
- `auth.js` - example signup/login (in-memory for demo). For production, replace with DB-backed auth.
- `payments.js` - creates Stripe Checkout Sessions. Requires `STRIPE_SECRET_KEY` env var.
- `stripeWebhook.js` - verifies Stripe webhook signatures. Requires `STRIPE_WEBHOOK_SECRET`.
- `agentWorkflow.js` - sample orchestration that calls external AI endpoints (placeholders).

Environment variables to set in Netlify (Site Settings → Build & deploy → Environment):
- `JWT_SECRET` - secret for signing JWTs (for demo auth)
- `STRIPE_SECRET_KEY` - your Stripe secret key
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook signing secret
- `FRONTEND_URL` - public frontend URL for success/cancel redirects
- `AI_QUALIFY_URL`, `AI_REHAB_URL` - optional external AI webhook URLs

Notes:
- These functions are examples to get you started. For production you'll need persistent storage (Postgres), proper key management, and secure verification.
- Keep secrets out of the repo. Use Netlify environment settings.
