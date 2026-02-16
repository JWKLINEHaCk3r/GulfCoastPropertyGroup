# 🚀 PRODUCTION DEPLOYMENT GUIDE - LIVE NOW

## ✅ GitHub Push Complete
All code is now at: **https://github.com/JWKLINEHaCk3r/GulfCoastPropertyGroup**

---

## 📋 DEPLOYMENT OPTIONS

### **OPTION 1: HEROKU (Easiest - Recommended)**
Heroku is the simplest for full deployment (frontend + backend together).

#### Step 1: Create Heroku Account
```bash
# Go to heroku.com and signup
# Install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Create Backend App
```bash
heroku login
heroku create gulf-coast-property-group-backend
```

#### Step 3: Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:standard-0 -a gulf-coast-property-group-backend
```

#### Step 4: Set Environment Variables
```bash
heroku config:set APP_ENV=production -a gulf-coast-property-group-backend
heroku config:set APP_NAME=GulfCoastPropertyGroup -a gulf-coast-property-group-backend
heroku config:set STRIPE_API_KEY=sk_live_xxxxxxxx -a gulf-coast-property-group-backend
heroku config:set STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxx -a gulf-coast-property-group-backend
heroku config:set OPENAI_API_KEY=sk-xxxxxxxx -a gulf-coast-property-group-backend
heroku config:set ANTHROPIC_API_KEY=sk-ant-xxxxxxxx -a gulf-coast-property-group-backend
heroku config:set SENDGRID_API_KEY=SG.xxxxxxxx -a gulf-coast-property-group-backend
heroku config:set TWILIO_ACCOUNT_SID=ACxxxxxxxx -a gulf-coast-property-group-backend
heroku config:set TWILIO_AUTH_TOKEN=xxxxxxxx -a gulf-coast-property-group-backend
heroku config:set JWT_SECRET=your_super_secret_key_here -a gulf-coast-property-group-backend
```

#### Step 5: Deploy Backend
```bash
cd backend
git push heroku main
heroku run "alembic upgrade head" -a gulf-coast-property-group-backend
heroku logs -f -a gulf-coast-property-group-backend
```

#### Step 6: Deploy Frontend to Netlify
```bash
cd ../frontend
npm install
npm run build

# Then go to Netlify and:
# 1. Import GitHub repository
# 2. Deploy branch: main
# 3. Build command: npm run build
# 4. Publish directory: dist
# 5. Environment variable: VITE_API_URL=https://gulf-coast-property-group-backend.herokuapp.com
```

---

### **OPTION 2: RAILWAY.APP (Modern Alternative - Recommended)**
Railway is newer, easier, better for development teams.

#### Step 1: Create Railway Account
Visit: **https://railway.app** and signup with GitHub

#### Step 2: Create New Project
```
Railway Dashboard → New Project → Deploy from GitHub Repo
Select: JWKLINEHaCk3r/GulfCoastPropertyGroup
```

#### Step 3: Configure Services
Railway will auto-detect:
- **Backend** (Python/FastAPI)
- **Database** (PostgreSQL - optional, can add)

#### Step 4: Set Environment Variables
In Railway dashboard, add these to Backend service:
```
APP_ENV=production
STRIPE_API_KEY=sk_live_xxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
SENDGRID_API_KEY=SG.xxxxxxxx
TWILIO_ACCOUNT_SID=ACxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxx
JWT_SECRET=your_super_secret
```

#### Step 5: Deploy
- Click "Generate Domain" 
- Note the backend URL (e.g., `railway-prod.up.railway.app`)
- Add to frontend as `VITE_API_URL`

---

### **OPTION 3: AWS (Enterprise Grade)**

#### Set up EC2 + RDS + Load Balancer
```bash
# 1. Create EC2 instance (Ubuntu 22.04, t3.large)
# 2. Create RDS PostgreSQL database
# 3. Configure security groups
# 4. Add Application Load Balancer
# 5. Add SSL certificate (AWS Certificate Manager)
# 6. Deploy backend via CodeDeploy or manual SSH
```

#### Deployment Script
```bash
ssh -i your-key.pem ec2-user@your-instance-ip

# On EC2:
git clone https://github.com/JWKLINEHaCk3r/GulfCoastPropertyGroup.git
cd real-estate-ecosystem/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgres://...
export STRIPE_API_KEY=sk_live_...
# ... set all env vars
alembic upgrade head
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app
```

---

## 🌐 NETLIFY FRONTEND DEPLOYMENT (All Options)

### Method 1: GitHub Auto-Deploy (Easiest)
```
1. Go to https://app.netlify.com
2. Click "Import an existing project"
3. Select GitHub as your git provider
4. Authorize Netlify
5. Select: JWKLINEHaCk3r/GulfCoastPropertyGroup
6. Configure build settings:
   - Build command: npm run build
   - Publish directory: frontend/dist
   - Base directory: frontend
7. Add environment variables:
   VITE_API_URL = https://your-backend-url.com
8. Click "Deploy"
```

### Method 2: Netlify CLI (For CI/CD)
```bash
npm install -g netlify-cli
netlify login
cd frontend
netlify deploy --prod --dir=dist
```

### Setting Custom Domain
```
Netlify Dashboard → Site Settings → Domain Management
→ Add custom domain → Configure DNS with your registrar
```

---

## 🗄️ DATABASE SETUP

### Using Heroku PostgreSQL
```bash
heroku pg:info -a gulf-coast-property-group-backend
# Database URL is automatically set as DATABASE_URL
heroku run "alembic upgrade head"
```

### Using Railway PostgreSQL
```
Railway Dashboard → Create new PostgreSQL plugin
Railway auto-creates DATABASE_URL environment variable
Run migrations from backend service terminal
```

### Using AWS RDS
```bash
# From your backend instance:
psql -h rds-instance-endpoint.amazonaws.com \
     -U postgres \
     -d propertydb
# Run migrations
alembic upgrade head
```

---

## ✅ POST-DEPLOYMENT CHECKLIST

### Test Backend
```bash
# Health check
curl https://your-backend-url.com/health
# Response: {"status": "OK"}

# Test auth endpoint
curl -X POST https://your-backend-url.com/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "company_name": "Test"
  }'

# Test agents endpoint
curl https://your-backend-url.com/api/v1/agents
```

### Test Frontend
- [ ] Can access https://your-domain.com
- [ ] Can view landing page
- [ ] Can click signup
- [ ] Can login successfully
- [ ] Can access dashboard
- [ ] Can see agents
- [ ] API calls work (check network tab)

### Test Payments
- [ ] Can view pricing page
- [ ] Can click "Subscribe"
- [ ] Stripe checkout loads
- [ ] Can use test card: `4242 4242 4242 4242`
- [ ] Webhook processes payment
- [ ] Confirmation email sent

### Test Email
- [ ] Signup confirmation email arrives
- [ ] Welcome email arrives
- [ ] Password reset works
- [ ] Admin notification sent

---

## 🔐 PRODUCTION SECURITY

### Enable SSL/TLS
```
Heroku:      Automatic (free)
Netlify:     Automatic (free)
Railway:     Automatic (free)
AWS:         AWS Certificate Manager (free)
```

### Set Headers
After deployment, add to backend `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### Enable Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginRequest):
    ...
```

---

## 📊 MONITORING & LOGGING

### Sentry Error Tracking
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/project",
    environment="production",
    traces_sample_rate=0.1,
)
```

### Heroku Logs
```bash
heroku logs -f -a gulf-coast-property-group-backend
```

### Railway Logs
```
Railway Dashboard → Backend Service → Logs tab
```

### AWS CloudWatch
```bash
aws logs tail /aws/ec2/property-group --follow
```

---

## 🚀 FIRST DAY LAUNCH CHECKLIST

- [ ] All code pushed to GitHub
- [ ] Backend deployed (Heroku/Railway/AWS)
- [ ] Frontend deployed (Netlify)
- [ ] Database migrations completed
- [ ] All endpoints tested
- [ ] SSL/TLS enabled
- [ ] Custom domain configured
- [ ] Email service (SendGrid) verified
- [ ] SMS service (Twilio) verified
- [ ] Payment webhook (Stripe) configured
- [ ] Error tracking (Sentry) active
- [ ] Analytics configured (Google Analytics)
- [ ] Alerts configured (email on errors)
- [ ] 100 beta users invited
- [ ] Monitoring dashboard open

---

## 🎯 DEPLOYMENT COMMANDS SUMMARY

### Quick Deploy (Heroku)
```bash
# Terminal 1: Backend
heroku login
cd backend
git push heroku main

# Wait for deployment...
heroku run "alembic upgrade head"
heroku open

# Terminal 2: Frontend
cd frontend
npm run build
# Deploy to Netlify via GitHub import

# Test
curl https://backend.herokuapp.com/health
```

### Quick Deploy (Railway)
```bash
# Push to GitHub
git push origin main

# Railway auto-deploys from GitHub webhook
# Check deployment status in Railway dashboard
# Copy backend URL
# Add to frontend VITE_API_URL
```

---

## 💰 ESTIMATED COSTS (First Month)

| Service | Price | Notes |
|---------|-------|-------|
| Heroku Backend | $50-100 | Pro dyno |
| Heroku Database | $50-200 | Standard tier |
| Netlify Frontend | Free | Included |
| SendGrid | $19 | 100K emails/month |
| Twilio | $1-50 | Pay per SMS |
| Stripe | 2.9% + 30¢ | Per transaction |
| **TOTAL** | **$120-400** | Depends on volume |

---

## 🆘 TROUBLESHOOTING

### "Backend won't start"
```bash
heroku logs -f
# Check config vars: heroku config
# Check Procfile exists in backend/
```

### "Database migration fails"
```bash
heroku run "alembic current"
heroku run "alembic upgrade head -v"
# Check database password, user permissions
```

### "Frontend can't reach backend"
```
1. Check VITE_API_URL in Netlify environment
2. Check CORS is enabled in backend
3. Check backend is actually running
4. Open DevTools → Network tab → see error
```

### "Payment webhook not working"
```bash
stripe listen --forward-to https://your-backend.com/webhooks/stripe
# Check STRIPE_WEBHOOK_SECRET is set correctly
# Check webhook endpoint exists in backend
```

---

## 🎉 YOU'RE LIVE!

Once all checks pass:
1. ✅ **Backend is live** at `https://backend-url.com`
2. ✅ **Frontend is live** at `https://frontend-domain.com`
3. ✅ **Database is live** with migrations applied
4. ✅ **Payments are live** (Stripe connected)
5. ✅ **Email is live** (SendGrid configured)
6. ✅ **AI agents are live** (models ready)
7. ✅ **Monitoring is live** (errors tracked)

**Now invite users and start generating revenue!**

---

## 📈 NEXT STEPS AFTER LAUNCH

1. **Invite Beta Users** (send emails to first 100)
2. **Launch Marketing Campaign** (Google Ads, Facebook Ads)
3. **Monitor Performance** (check logs, errors, response times)
4. **Scale Infrastructure** (increase dyno size if needed)
5. **Improve Agents** (add real LLM calls, fine-tune)
6. **Expand Features** (add advanced features from roadmap)
7. **Global Expansion** (add countries and languages)

---

**Questions?** Check `QUICK_START_DEPLOYMENT.md` for more details.

**Status**: 🟢 Ready to Deploy
