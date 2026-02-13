# Netlify Build Settings - Quick Reference Card

## Copy & Paste These Values into Netlify

### 1. Build Settings (Site Settings → Build & Deploy)

| Field | Value |
|-------|-------|
| **Branch to deploy** | `main` |
| **Base directory** | `frontend` |
| **Build command** | `npm ci && npm run build` |
| **Publish directory** | `dist` |
| **Functions directory** | `netlify/functions` |

---

## 2. Environment Variables (Site Settings → Build & Deploy → Environment)

Add these environment variables to enable production deployment:

### Required Variables

```
VITE_API_BASE_URL          https://api.yourdomain.com
VITE_ENVIRONMENT           production
```

### Optional Variables (for enhanced features)

```
VITE_SENTRY_DSN            https://[your-sentry-key]@sentry.io/[project-id]
VITE_GA_TRACKING_ID        UA-XXXXXXXXX-X
```

### Feature Flag Variables (set true/false)

```
VITE_ENABLE_LEAD_SCOUT             true
VITE_ENABLE_OFFER_GENERATOR        true
VITE_ENABLE_BUYER_MATCHER          true
VITE_ENABLE_NEGOTIATION_ASSISTANT  true
VITE_ENABLE_SEO_CONTENT            true
```

---

## 3. Node Configuration (Auto-detected from netlify.toml)

**Node Version**: 18.17.0  
**NPM Version**: 9.6.7+  
**Package Manager**: npm

---

## 4. Post-Deployment Configuration

After Netlify builds successfully:

### Connect Custom Domain
1. Site Settings → Domain Management
2. Add custom domain
3. Update DNS records (CNAME or A)

### Enable Auto-SSL
- Automatic (within 24 hours)
- Verify at: Site Settings → Domain Management

### Set Up Continuous Deployment
- Already configured in `netlify.toml`
- Every push to `main` triggers automatic build

---

## 5. Key Files That Enable This Build

These files work together to configure your build:

| File | Purpose |
|------|---------|
| `netlify.toml` | Main build configuration (root directory) |
| `frontend/package.json` | Node dependencies and build scripts |
| `frontend/vite.config.js` | Vite build tool configuration |
| `.netlifyignore` | Files to exclude from build |
| `frontend/.env.netlify` | Environment variable template |

---

## 6. Build Process Timeline

```
GitHub push → Webhook to Netlify → Detect netlify.toml
      ↓
Run: npm ci (install dependencies from package.json)
      ↓
Run: npm run build (Vite compiles src → dist)
      ↓
Deploy dist/ to Netlify CDN
      ↓
Apply redirects & headers from netlify.toml
      ↓
LIVE: https://yourdomain.com ✅
```

**Build Time**: 45-60 seconds  
**Deployment Time**: 30-60 seconds  
**Total**: ~2 minutes from push to live

---

## 7. Testing Before Production

### 1. Local Build Test
```bash
cd frontend
npm ci
npm run build
npm run preview
# Visit: http://localhost:3000
```

### 2. Branch Deploy Test
```bash
git checkout -b test-deployment
git push origin test-deployment
# View preview URL in Netlify Deploy logs
```

### 3. Production Deploy
```bash
git push origin main
# View at: https://yourdomain.com
```

---

## 8. Troubleshooting Quick Links

**Build Logs**: Site → Deploys → [Latest] → View full logs

**Common Issues**:
- `npm: command not found` → Check Node version in netlify.toml
- `Cannot find module` → Ensure frontend/package.json exists
- `ENOENT no dist` → Verify frontend/vite.config.js outDir setting

---

## 9. Monitoring After Deployment

### Check Build Status
- Netlify Dashboard → Deploys
- Shows build time, success/failure, logs

### Monitor Frontend Performance
- Netlify Analytics → Analytics tab
- Shows traffic, page views, bounce rate

### Monitor Backend Connectivity
- Test API calls: `curl https://yourdomain.com/api/health`
- Check CORS headers if connection fails

---

## 10. Rollback to Previous Deployment

If something breaks:

1. Netlify Dashboard → Deploys
2. Find previous successful deploy
3. Click "Publish this deploy"
4. Site reverts to previous version instantly

---

## 11. Advanced: Custom Build Scripts

If you need different build for different branches:

```toml
# In netlify.toml

[context.production]
  command = "npm run build"

[context.branch-deploy]
  command = "npm run build:staging"

[context.deploy-preview]
  command = "npm run build:preview"
```

---

## 12. Deploy Status Badges (Optional)

Add to your README.md:

```markdown
[![Netlify Status](https://api.netlify.com/api/v1/badges/YOUR-SITE-ID/deploy-status)](https://app.netlify.com/sites/your-site-name/deploys)
```

(Replace YOUR-SITE-ID from Netlify dashboard)

---

## Ready to Deploy?

✅ All configuration files are in place  
✅ Package.json has all dependencies  
✅ netlify.toml has all build settings  
✅ Environment variables documented  

**Next Step**: Push to GitHub and connect to Netlify!

```bash
git add .
git commit -m "Add Netlify deployment configuration"
git push origin main
```

Then visit: **https://app.netlify.com** and "Import an existing project"

---

**Questions?** See docs/NETLIFY_DEPLOYMENT.md for detailed guide.
