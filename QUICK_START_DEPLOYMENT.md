"""
QUICK START DEPLOYMENT GUIDE
Do this FIRST to get platform live (today/tomorrow)
"""

# ==================== BEFORE YOU START ====================

REQUIREMENTS = {
    'time_estimated': '6-8 hours',
    'skills_needed': 'Basic terminal, basic Python, basic deployment',
    'prerequisites': [
        'GitHub account (for pushing code)',
        'Heroku account (or AWS, GCP)',
        'Netlify account (for frontend)',
        'API keys:',
        '  - Stripe (production)',
        '  - OpenAI',
        '  - Anthropic',
        '  - SendGrid',
        '  - Twilio',
    ]
}

# ==================== STEP-BY-STEP DEPLOYMENT ====================

DEPLOYMENT_STEPS = [
    {
        'step': 1,
        'title': 'Setup Environment Variables',
        'instructions': [
            '1. Copy backend/.env.example to backend/.env',
            '2. Fill in ALL variables:',
            '   APP_NAME=GulfCoastPropertyGroup',
            '   APP_ENV=production',
            '   DATABASE_URL=postgres://...',
            '   STRIPE_API_KEY=sk_live_...',
            '   STRIPE_WEBHOOK_SECRET=whsec_...',
            '   OPENAI_API_KEY=sk-...',
            '   ANTHROPIC_API_KEY=sk-ant-...',
            '   SENDGRID_API_KEY=SG....',
            '   TWILIO_ACCOUNT_SID=AC...',
            '   TWILIO_AUTH_TOKEN=...',
            '3. Save to safe location (password manager)',
        ],
        'time_minutes': 15,
        'critical': True,
    },
    {
        'step': 2,
        'title': 'Setup Database',
        'instructions': [
            '1. Create PostgreSQL database:',
            '   - AWS RDS: 20GB storage, Multi-AZ',
            '   - GCP Cloud SQL: 20GB storage',
            '   - Heroku Postgres: Standard-2',
            '2. Get connection string',
            '3. Export DATABASE_URL env var',
            '4. Run migrations:',
            '   cd backend',
            '   pip install alembic sqlalchemy',
            '   alembic upgrade head',
        ],
        'time_minutes': 30,
        'critical': True,
    },
    {
        'step': 3,
        'title': 'Deploy Backend',
        'instructions': [
            'Option A: Heroku (Easiest)',
            '  1. heroku create your-app-name',
            '  2. heroku config:set VAR_NAME=value (for each env var)',
            '  3. git push heroku main',
            '  4. heroku logs -f  # Watch it deploy',
            '',
            'Option B: AWS ECS',
            '  1. Build Docker image: docker build -t backend .',
            '  2. Push to ECR',
            '  3. Create ECS task definition',
            '  4. Setup load balancer',
            '  5. Deploy',
            '',
            'Option C: Google Cloud Run',
            '  1. gcloud builds submit --tag gcr.io/PROJECT/backend',
            '  2. gcloud run deploy backend --image gcr.io/PROJECT/backend',
        ],
        'time_minutes': 20,
        'critical': True,
    },
    {
        'step': 4,
        'title': 'Deploy Frontend',
        'instructions': [
            '1. cd frontend',
            '2. npm install',
            '3. npm run build',
            '4. Connect to Netlify:',
            '   - Import from Git (GitHub)',
            '   - Set build command: npm run build',
            '   - Set publish directory: dist',
            '   - Set environment: VITE_API_URL=https://backend-url.com',
            '5. Deploy',
            '6. Setup custom domain',
            '7. Enable CDN caching',
        ],
        'time_minutes': 15,
        'critical': True,
    },
    {
        'step': 5,
        'title': 'Test Backend Endpoints',
        'instructions': [
            'Open Postman or Insomnia',
            '',
            'Test Authentication:',
            '  POST /auth/signup',
            '  {',
            '    "email": "test@example.com",',
            '    "password": "SecurePassword123!",',
            '    "company_name": "Test Company"',
            '  }',
            '',
            'Test Payment Endpoint:',
            '  GET /subscriptions/plans',
            '',
            'Test Agents:',
            '  GET /agents/',
            '  POST /agents/lead-qualifier/qualify',
            '',
            'If all return 200: ✅ Backend working!',
        ],
        'time_minutes': 15,
        'critical': True,
    },
    {
        'step': 6,
        'title': 'Setup Stripe Webhook',
        'instructions': [
            '1. Go to Stripe Dashboard',
            '2. Developers > Webhooks',
            '3. Create endpoint:',
            '   URL: https://your-backend.com/webhooks/stripe',
            '   Events: payment_intent.succeeded, customer.subscription.created',
            '4. Copy webhook secret',
            '5. Add to environment: STRIPE_WEBHOOK_SECRET=',
            '6. Deploy backend again',
        ],
        'time_minutes': 10,
        'critical': True,
    },
    {
        'step': 7,
        'title': 'Beta Test with Live Data',
        'instructions': [
            '1. Signup at https://your-domain.com',
            '2. Test payment flow:',
            '   - Click Subscribe',
            '   - Use Stripe test card: 4242 4242 4242 4242',
            '   - Should get confirmation email',
            '3. Test agent workflows:',
            '   - Go to Dashboard',
            '   - Click "Find Deals"',
            '   - Agents should start working',
            '4. Invite 50-100 beta users',
            '5. Collect feedback',
        ],
        'time_minutes': 30,
        'critical': True,
    },
    {
        'step': 8,
        'title': 'Setup Monitoring & Alerts',
        'instructions': [
            'Sentry (Error Tracking):',
            '  1. Create account at sentry.io',
            '  2. Create project',
            '  3. Add to backend requirements: sentry-sdk',
            '  4. Initialize in main.py',
            '',
            'Datadog (Performance Monitoring):',
            '  1. Create account at datadoghq.com',
            '  2. Install agent',
            '  3. Monitor API response times',
            '  4. Setup alerts for errors > 1%',
            '',
            'AWS CloudWatch (if on AWS):',
            '  1. Enable CloudWatch logs',
            '  2. Setup alarms for high CPU/memory',
            '  3. Setup SNS notifications',
        ],
        'time_minutes': 20,
        'critical': True,
    },
    {
        'step': 9,
        'title': 'Launch Marketing Website',
        'instructions': [
            '1. Update homepage with:',
            '   - Product benefits',
            '   - Pricing',
            '   - CTA button',
            '2. Setup landing page:',
            '   - Headline: "Real Estate Deals Closed in 3 Days"',
            '   - CTA: "Start Free Trial"',
            '3. Setup analytics:',
            '   - Add Google Analytics tracking',
            '   - Add Hotjar for user behavior',
            '   - Add Mixpanel for funnel analytics',
            '4. Setup email capture:',
            '   - Homepage email signup',
            '   - Send welcome email via Sendgrid',
        ],
        'time_minutes': 20,
        'critical': False,
    },
    {
        'step': 10,
        'title': 'First Marketing Campaign',
        'instructions': [
            '1. Create Google Ads account',
            '2. Setup search campaign:',
            '   - Keywords: real estate investing, find deals, etc',
            '   - Budget: $1,000/day',
            '   - Target CPA: $75',
            '3. Create Facebook/Instagram ads',
            '4. Create landing page with offer:',
            '   - "$1,000 in free leads" for signing up',
            '5. Launch in #1 target market (California)',
            '6. Monitor CAC (Customer Acquisition Cost)',
        ],
        'time_minutes': 30,
        'critical': False,
    },
]

# ==================== VERIFICATION CHECKLIST ====================

VERIFICATION_CHECKLIST = """
✅ DEPLOYMENT VERIFICATION

□ Backend deployed and running
  □ Can access /health endpoint
  □ Database migrations completed successfully
  □ All environment variables set
  
□ Frontend deployed and accessible
  □ Can load homepage
  □ All links work
  □ Can signup and login
  
□ Payment system working
  □ Stripe webhook configured
  □ Can subscribe to plan
  □ Receive confirmation email
  
□ Agents working
  □ Agent endpoints respond
  □ Can trigger lead discovery
  □ Seeing deal data in dashboard
  
□ Monitoring active
  □ Sentry tracking errors
  □ CloudWatch tracking performance
  □ Alerts configured
  
□ Security configured
  □ SSL/TLS enabled
  □ CORS configured
  □ Rate limiting enabled
  □ Input validation working
  
□ Domain & branding
  □ Custom domain working
  □ Logo displayed
  □ Brand colors applied
  □ All copy updated
"""

# ==================== TROUBLESHOOTING ====================

TROUBLESHOOTING = {
    'problem': 'Backend won\'t start',
    'solutions': [
        'Check Python version: python --version (need 3.9+)',
        'Check requirements installed: pip install -r requirements.txt',
        'Check database connection: Check DATABASE_URL is correct',
        'Check env vars: Print all vars and verify they\'re set',
        'Check logs: Look at deployment logs for specific error',
    ],
    'problem': 'Database migrations fail',
    'solutions': [
        'Make sure database exists and is accessible',
        'Run: alembic upgrade head -v (verbose mode)',
        'Check database user has create table permissions',
        'Drop and recreate database if needed (dev only):',
        '  dropdb dbname && createdb dbname',
    ],
    'problem': 'Payment not working',
    'solutions': [
        'Check Stripe API key is correct (sk_live_, not sk_test_)',
        'Check webhook secret is set',
        'Check Stripe account is in live mode',
        'Test with Stripe CLI: stripe listen',
        'Check payment endpoint in logs',
    ],
    'problem': 'Frontend can\'t connect to backend',
    'solutions': [
        'Check VITE_API_URL env var is correct',
        'Check backend is running and accessible',
        'Check CORS is enabled: app.add_middleware(CORSMiddleware)',
        'Check firewall isn\'t blocking connection',
        'Check console for exact error message',
    ],
}

# ==================== POST-DEPLOYMENT ====================

POST_DEPLOYMENT = {
    'day_1': [
        'Monitor error rates (should be < 0.1%)',
        'Test with real user signup',
        'Monitor database performance',
        'Check Stripe transactions',
        'Invite 50 beta users',
    ],
    'day_2': [
        'Monitor NPS from beta users',
        'Fix any bugs found',
        'Scale database if needed',
        'Collect feedback',
        'Invite 100 more users',
    ],
    'day_3': [
        'Launch public marketing campaign',
        'Start content creation',
        'Deploy autonomous agent improvements',
        'Scale infrastructure to 10x current capacity',
        'Prepare for growth',
    ],
    'week_1': [
        'Reach 10,000 signup (target)',
        'Process first 100 deals',
        'Generate $50K+ revenue',
        'NPS should be 60+',
        'Retention rate should be 80%+',
    ],
    'month_1': [
        'Reach 100,000 users',
        'Process 1,000+ deals',
        'Generate $500K revenue',
        'Scale to handle 10x growth',
        'Implement first set of improvements',
    ],
}

# ==================== ESTIMATED COSTS ====================

ESTIMATED_FIRST_MONTH_COSTS = {
    'server': {
        'backend': 5_000,  # Heroku/AWS ECS
        'database': 3_000,  # RDS/Cloud SQL
        'cdn': 500,  # Cloud Front / Cloudflare
    },
    'services': {
        'stripe_fees': 2_000,  # 2.9% + 30¢ per transaction
        'twilio_sms': 1_000,
        'sendgrid': 500,
        'opensearch': 1_000,
    },
    'apis': {
        'openai': 2_000,
        'anthropic': 1_000,
        'google_maps': 500,
    },
    'monitoring': {
        'datadog': 500,
        'sentry': 300,
    },
    'marketing': {
        'google_ads': 10_000,
        'facebook_ads': 5_000,
    },
    'total_first_month': 31_800,
    'note': 'Costs will decrease as % of revenue after Month 1',
}

# ==================== SUCCESS CRITERIA ====================

SUCCESS_CRITERIA = """
🎯 YOU'LL KNOW IT'S WORKING WHEN:

✅ Week 1:
   - 5,000+ signups
   - 50+ deals in pipeline
   - $50,000+ revenue
   - 0 critical bugs
   - 99.9% uptime

✅ Month 1:
   - 100,000+ users
   - 1,000+ deals closed
   - $500,000+ revenue
   - 70+ NPS
   - 99.95% uptime

✅ Month 3:
   - 500,000+ users
   - 10,000+ deals closed
   - $5,000,000+ revenue
   - 75+ NPS
   - Ranked #1 in category

✅ Year 1:
   - 1,000,000+ users
   - 100,000+ deals closed
   - $100,000,000+ revenue
   - 85+ NPS
   - $500M+ valuation
"""

# ==================== FINAL DEPLOYMENT COMMAND ====================

DEPLOYMENT_COMMANDS = """
👉 COPY & PASTE - DEPLOYMENT COMMANDS:

# 1. Setup environment
export APP_ENV=production
export DATABASE_URL=postgres://...
export STRIPE_API_KEY=sk_live_...
# (set all other env vars)

# 2. Deploy backend (Heroku example)
cd backend
heroku create your-app-name
git push heroku main
heroku logs -f

# 3. Deploy migrations
heroku run "alembic upgrade head"

# 4. Deploy frontend
cd ../frontend
npm install
npm run build
# (Push to Netlify via git)

# 5. Verify
curl https://your-backend.com/health
# Should return: {"status": "OK"}

# 6. Open in browser
open https://your-frontend.com

# 🎉 LIVE!
"""
