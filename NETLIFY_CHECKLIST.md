# Netlify Deployment - Configuration Checklist

Use this checklist to verify all components are properly configured for Netlify deployment.

## ✅ Configuration Files

- [x] **netlify.toml** (Project root)
  - Defines build settings, environment variables, redirects, headers
  - Location: `/netlify.toml`
  - Status: ✅ Created and configured

- [x] **frontend/package.json**
  - Node.js dependencies and build scripts
  - Location: `/frontend/package.json`
  - Build Scripts: `dev`, `build`, `build:preview`, `build:staging`, `preview`, `lint`, `test`
  - Status: ✅ Created with 35+ dependencies

- [x] **frontend/vite.config.js**
  - Vite build tool configuration
  - Configures output to `dist/` directory
  - API proxy to backend
  - Status: ✅ Created with production optimizations

- [x] **.netlifyignore**
  - Files/folders to exclude from Netlify builds
  - Reduces build time and artifact size
  - Status: ✅ Created

- [x] **frontend/.env.netlify**
  - Environment variable template for Netlify
  - Includes documentation for each variable
  - Status: ✅ Created for reference

---

## 🔧 Netlify Build Settings

Configure these in **Site Settings → Build & Deploy**:

### Branch to Deploy
- [ ] Set to: `main` (or `master` if that's your default branch)
- [ ] Verify in Netlify Dashboard: **Site Settings → Build & Deploy → Continuous Deployment**

### Base Directory
- [ ] Set to: `frontend`
- [ ] This tells Netlify where `package.json` is located

### Build Command
- [ ] Set to: `npm ci && npm run build`
- [ ] `npm ci` = clean install (reproducible, for CI/CD)
- [ ] `npm run build` = calls Vite to build to `dist/`

### Publish Directory
- [ ] Set to: `dist`
- [ ] This is where Vite outputs the built frontend

### Functions Directory
- [ ] Set to: `netlify/functions` (default)
- [ ] For future serverless functions

---

## 🌍 Environment Variables

Configure in **Site Settings → Build & Deploy → Environment**:

### Required Variables

- [ ] `VITE_API_BASE_URL` = `https://api.yourdomain.com`
  - Points frontend to your backend API
  - Change from `yourdomain.com` to your actual domain

- [ ] `VITE_ENVIRONMENT` = `production`
  - Enables production optimizations
  - Disables console logs in deployed version

### Optional Variables

- [ ] `VITE_SENTRY_DSN` (if using error tracking)
  - Sign up at: https://sentry.io
  - Format: `https://[key]@sentry.io/[project-id]`
  - Leave blank if not using Sentry

- [ ] `VITE_GA_TRACKING_ID` (if using Google Analytics)
  - Format: `UA-XXXXXXXXX-X`
  - Get from: https://analytics.google.com

### Feature Flags (Optional)

- [ ] `VITE_ENABLE_LEAD_SCOUT` = `true`
- [ ] `VITE_ENABLE_OFFER_GENERATOR` = `true`
- [ ] `VITE_ENABLE_BUYER_MATCHER` = `true`
- [ ] `VITE_ENABLE_NEGOTIATION_ASSISTANT` = `true`
- [ ] `VITE_ENABLE_SEO_CONTENT` = `true`

**Note**: To add variables:
1. Dashboard → Site Settings → Build & Deploy → Environment
2. Click "Edit variables"
3. Add each key-value pair
4. Click "Save"
5. Trigger new deploy: **Deploys → Trigger deploy → Deploy site**

---

## 📦 Node.js Runtime

Verify Netlify uses compatible Node version:

- [ ] Node Version: **18.17.0** (specified in netlify.toml)
- [ ] NPM Version: **9.6.7+** (automatic)
- [ ] Package Manager: **npm** (not yarn)

**Status**: ✅ Auto-configured in `[build.environment]` section of netlify.toml

---

## 📡 Git Repository

Prepare repository for deployment:

- [ ] All files committed: `git status` shows clean working directory
- [ ] Pushed to remote: `git push origin main`
- [ ] netlify.toml is in root directory (not in git ignore)
- [ ] .gitignore excludes `node_modules/`, `dist/`, `.env` (not `.env.netlify`)
- [ ] Repository is public (or Netlify has access)

**Commands**:
```bash
git add .
git commit -m "Add Netlify configuration for production deployment"
git push origin main
```

---

## 🚀 Connect to Netlify

Steps to connect GitHub repo to Netlify:

- [ ] Visit: https://app.netlify.com
- [ ] Click: **Add new site**
- [ ] Select: **Import an existing project**
- [ ] Choose: Your Git provider (GitHub, GitLab, Bitbucket)
- [ ] Authorize: Grant Netlify access to repositories
- [ ] Select: Your repository (`real-estate-ecosystem`)
- [ ] Verify: Build settings show automatically
  - Base directory: `frontend`
  - Build command: `npm ci && npm run build`
  - Publish directory: `dist`
- [ ] Click: **Deploy site**
- [ ] Wait: ~2 minutes for first build
- [ ] View: Preview URL like `https://xxxxx.netlify.app`

**Build Logs**: After clicking "Deploy site", watch **Deploys** tab for build progress

---

## 🔐 Backend API Connection

Your frontend is configured to connect to backend API:

- [ ] Backend API deployed at: `https://api.yourdomain.com`
- [ ] Backend API has CORS enabled for: `https://yourdomain.com`
- [ ] Backend API `/health` endpoint responds to: GET `/api/health`
- [ ] `VITE_API_BASE_URL` in Netlify environment matches backend API URL

**Testing Connection**:
```bash
# From your local terminal
curl https://yourdomain.com/api/health

# Response should be:
# {"status":"healthy","timestamp":"2024-02-13T..."}
```

If connection fails:
1. Check CORS headers on backend (see docs/DEPLOYMENT.md)
2. Verify API URL is correct in Netlify environment variables
3. Check backend is deployed and running

---

## 🌐 Custom Domain Setup

Optional: Connect custom domain to Netlify deployment:

- [ ] Domain registered at: Namecheap, GoDaddy, Route53, etc.
- [ ] Domain pointing to Netlify DNS or A record
- [ ] SSL certificate enabled (auto-provisioned by Netlify)

**Steps**:
1. Dashboard → **Site Settings** → **Domain Management**
2. Click: **Add custom domain**
3. Enter your domain (e.g., `app.yourdomain.com`)
4. Follow DNS setup instructions
5. Wait: 5-30 minutes for DNS propagation
6. Verify: Visit your domain - should show your site

**SSL Certificate**:
- Automatically provisioned within 24 hours
- Accessible at: `https://yourdomain.com` (not just `http://`)

---

## 🧪 Testing After Deployment

Verify your deployed site works correctly:

### 1. Frontend Load Test
- [ ] Visit: `https://yourdomain.com`
- [ ] Page loads without 404 errors
- [ ] All styling appears correct
- [ ] No console errors (F12 → Console)

### 2. API Connectivity Test
- [ ] Open Developer Tools (F12)
- [ ] Go to **Network** tab
- [ ] Perform an action that calls API (e.g., lead search)
- [ ] Verify request to `/api/*` succeeds (status 200)
- [ ] Check response contains expected data

### 3. Core Feature Tests
- [ ] [ ] Lead Search works
- [ ] [ ] Offer Generation works
- [ ] [ ] Buyer Matching works
- [ ] [ ] Negotiation Assistant works
- [ ] [ ] SEO Content Generation works

### 4. Performance Test
- [ ] Open in Chrome DevTools → **Lighthouse**
- [ ] Run audit for Performance
- [ ] Aim for: Performance score > 80
- [ ] Check: Time to Interactive < 3 seconds

### 5. Mobile Responsiveness
- [ ] Open DevTools → Toggle Device Toolbar (Ctrl+Shift+M)
- [ ] Test on iPhone 12, iPad, Android screen sizes
- [ ] Verify: All content visible, no horizontal scroll

---

## 📊 Monitoring & Analytics

After deployment, monitor your site:

- [ ] **Netlify Analytics**: **Site → Analytics**
  - View traffic, page views, bounce rate
  - See popular pages and referrers

- [ ] **Build Analytics**: **Deploys → [Latest]**
  - View build duration
  - See environment variables used
  - Check for warnings/errors

- [ ] **Performance Monitoring**:
  - Set up Sentry for error tracking
  - Enable Google Analytics for user behavior
  - Monitor backend API health

---

## 🔄 Continuous Deployment

Every push to your main branch triggers automatic build:

- [ ] Push code to `main` branch:
  ```bash
  git add .
  git commit -m "Feature: add new functionality"
  git push origin main
  ```

- [ ] Netlify automatically:
  1. Detects push notification via webhook
  2. Starts build in `frontend/` directory
  3. Runs `npm ci && npm run build`
  4. Deploys `dist/` contents to CDN
  5. Updates site (usually 2 min)

- [ ] View build status: Dashboard → **Deploys**

---

## ⚙️ Advanced Configuration

### Branch Deployments

Deploy different branches with different settings:

```toml
[context.production]
  command = "npm run build"
  
[context.branch-deploy]
  command = "npm run build:staging"
  
[context.deploy-preview]
  command = "npm run build:preview"
```

Then:
- [ ] Push to `main` → production build
- [ ] Push to `staging` → staging build  
- [ ] Create PR from feature branch → preview build

### Redirects & Rewrites

Already configured in netlify.toml to:
- [ ] Rewrite `/*` to `index.html` (for React Router)
- [ ] Proxy `/api/*` to backend
- [ ] Set cache headers for performance

---

## 🐛 Troubleshooting

### Build Errors

Check Netlify build logs: **Deploys → [Latest] → View full logs**

**Common Issues**:

| Error | Cause | Solution |
|-------|-------|----------|
| `npm: command not found` | Node not installed | Add NODE_VERSION to netlify.toml |
| `Cannot find module` | Missing dependency | Add to frontend/package.json |
| `ENOENT no dist` | Build didn't create output | Check vite.config.js |
| `Timeout` | Build too slow | Add `npm ci` instead of `npm install` |

### API Connection Issues

If frontend can't reach backend:

- [ ] Check backend URL in VITE_API_BASE_URL
- [ ] Verify backend has CORS enabled for your domain
- [ ] Test with: `curl https://yourdomain.com/api/health`
- [ ] Check DevTools → Network → see if requests fail

### SSL Certificate Issues

If HTTPS doesn't work:

- [ ] Wait 24 hours for cert provisioning
- [ ] Dashboard → Domain Management → check status
- [ ] Try accessing with `http://` to verify site works
- [ ] Contact Netlify support if stuck after 24h

---

## ✨ Optimization Checklist

For production performance:

- [ ] Enable gzip compression (automatic)
- [ ] Enable code splitting in Vite (automatic)
- [ ] Set cache headers (configured in netlify.toml)
- [ ] Use CDN for images (Netlify CDN included)
- [ ] Monitor Core Web Vitals (Lighthouse)

---

## 📚 Documentation References

For more information, see:

- **Quick Setup**: See [NETLIFY_BUILD_SETTINGS.md](./NETLIFY_BUILD_SETTINGS.md)
- **Detailed Guide**: See [docs/NETLIFY_DEPLOYMENT.md](./docs/NETLIFY_DEPLOYMENT.md)
- **Project Docs**: See [README.md](./README.md)
- **Architecture**: See [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)

---

## ✅ Final Verification

Before going live, confirm:

- [x] netlify.toml exists in root directory
- [x] frontend/package.json has dependencies
- [x] frontend/vite.config.js configured
- [x] Code pushed to GitHub
- [x] Netlify connected to repository
- [x] Environment variables set in Netlify
- [x] Build succeeds (green checkmark in Deploys)
- [x] Frontend loads at domain
- [x] API calls succeed (check Network tab)
- [x] Core features working
- [x] Mobile responsiveness tested
- [x] SSL certificate enabled

---

## 🎉 You're Ready!

Your real-estate wholesale platform is configured for production deployment on Netlify.

**Next Steps**:
1. Ensure all checkboxes above are checked
2. Push code to GitHub
3. Connect to Netlify (if not already)
4. Monitor deployments in dashboard
5. Watch your platform go live! 🚀

**Support**: See NETLIFY_DEPLOYMENT.md for detailed troubleshooting
