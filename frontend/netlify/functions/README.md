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

How to configure environment variables
 - Locally: copy `backend/.env.example` to `backend/.env` and fill real values. Do NOT commit actual keys.
 - Netlify: In your Site settings → Build & deploy → Environment → Environment variables, add the variables from `backend/.env.example` (for example `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `JWT_SECRET`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `FRONTEND_URL`).
 - For webhook verification: set `STRIPE_WEBHOOK_SECRET` to the value from your Stripe dashboard and ensure Netlify delivers the raw request body to the function (Netlify Functions SDK does this by default).

Recommended minimal env vars for production
 - `SECRET_KEY` (backend app)
 - `JWT_SECRET` (functions auth)
 - `STRIPE_SECRET_KEY`
 - `STRIPE_WEBHOOK_SECRET`
 - `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
 - `FRONTEND_URL`

Security notes
 - Never store secrets in the repo. If a secret was accidentally committed, rotate it immediately.
 - Use a secrets manager (Netlify environment variables, HashiCorp Vault, AWS Secrets Manager) for production.
