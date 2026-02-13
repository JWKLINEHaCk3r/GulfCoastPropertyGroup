# Netlify Build & Deployment Configuration Guide

This guide provides step-by-step instructions for deploying the Real Estate Wholesale Platform to Netlify.

## Quick Setup Summary

| Setting | Value |
|---------|-------|
| **Base Directory** | `frontend` |
| **Build Command** | `npm ci && npm run build` |
| **Publish Directory** | `dist` |
| **Functions Directory** | `netlify/functions` |
| **Node Version** | 18.17.0 |
| **Package Manager** | npm version 9.6.7+ |

## Netlify Configuration Files

### 1. **netlify.toml** (Already Created)
Main configuration file at project root. Contains:
- Build settings (base, command, publish directories)
- Environment variables for different contexts
- Redirect rules for React Router SPA
- Cache headers for optimized performance
- Security headers
- Context-specific builds (production, staging, preview)

### 2. **frontend/package.json** (Already Created)
Node.js dependencies and build scripts:
- **Build Scripts**:
  - `npm run build` - Production build
  - `npm run build:preview` - Preview deployment build
  - `npm run build:staging` - Staging deployment build
  - `npm run dev` - Local development
  
- **Key Dependencies**:
  - Vue 3.3.4
  - Vite (fast build tool)
  - TailwindCSS (styling)
  - Axios (API calls)
  - Chart.js (analytics visualization)
  - Various Vue plugins

### 3. **frontend/vite.config.js** (Already Created)
Vite build configuration:
- Source maps for development
- Code splitting and chunking
- Asset optimization
- API proxy configuration
- Development server on port 3000

### 4. **.netlifyignore** (Already Created)
Excludes unnecessary files from build:
- Node modules (downloaded fresh during build)
- Backend code (separate Netlify deployment)
- Temporary files
- Documentation

---

## Required Environment Variables

Configure these in Netlify UI under **Site Settings → Build & Deploy → Environment**

### Frontend Environment Variables

Set these for your Netlify deployment:

```
# API Configuration
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_ENVIRONMENT=production

# Optional: Analytics & Monitoring
VITE_SENTRY_DSN=https://your-sentry-key@sentry.io/project-id
VITE_GA_TRACKING_ID=UA-XXXXXXXXX-X

# Optional: Feature Flags
VITE_ENABLE_LEAD_SCOUT=true
VITE_ENABLE_OFFER_GENERATOR=true
VITE_ENABLE_BUYER_MATCHER=true
VITE_ENABLE_NEGOTIATION_ASSISTANT=true
VITE_ENABLE_SEO_CONTENT=true
```

### How to Set Environment Variables in Netlify:

1. Log in to Netlify Dashboard
2. Navigate to **Site Settings** → **Build & Deploy** → **Environment**
3. Click **Edit Variables**
4. Add each variable:
   - **Key**: (variable name)
   - **Value**: (variable value)
5. Click **Save**
6. Trigger a new deploy from **Deploys** → **Trigger deploy**

---

## Build Process Flow

```
Netlify Deployment Process:
┌─────────────────────────────────────────────────────────────┐
│1. GitHub/GitLab push to 'main' or 'master' branch           │
│                          ↓                                   │
│2. Netlify detects changes and starts build                  │
│                          ↓                                   │
│3. Checkout code to build directory                          │
│                          ↓                                   │
│4. Change to 'frontend' base directory                       │
│                          ↓                                   │
│5. Run: npm ci (clean install, no package-lock.json updates) │
│                          ↓                                   │
│6. Run: npm run build (Vite builds to 'dist' folder)         │
│                          ↓                                   │
│7. Deploy contents of 'dist' folder to CDN                   │
│                          ↓                                   │
│8. Configure redirects & headers from netlify.toml            │
│                          ↓                                   │
│9. Create preview URL for testing                            │
│                          ↓                                   │
│10. Publish to production domain                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Deployment Instructions

### Step 1: Prepare Repository

```bash
# Ensure code is committed and pushed to GitHub/GitLab
git add .
git commit -m "Add Netlify configuration for deployment"
git push origin main
```

### Step 2: Connect to Netlify

1. Visit **https://app.netlify.com**
2. Click **Add new site** → **Import an existing project**
3. Select your Git provider (GitHub, GitLab, Bitbucket)
4. Authorize Netlify to access your repositories
5. Select the repository: `your-username/real-estate-ecosystem`
6. Click **Next**

### Step 3: Configure Build Settings

Netlify will auto-detect `netlify.toml`. Verify these settings display:

- **Branch to deploy**: `main` (or `master`)
- **Base directory**: `frontend`
- **Build command**: `npm ci && npm run build`
- **Publish directory**: `dist`
- **Functions directory**: `netlify/functions`

Click **Deploy site** if settings are correct. Netlify will show a generated subdomain URL like:
```
https://your-site-random-id.netlify.app
```

### Step 4: Configure Environment Variables

After initial deployment:

1. Go to **Site Settings** → **Build & Deploy** → **Environment**
2. Add the variables from the "Required Environment Variables" section above
3. Under **Build & Deploy** → **Branches**, ensure `main` is set to auto-publish
4. Trigger a manual rebuild: **Deploys** → **Trigger deploy** → **Deploy site**

### Step 5: Configure Custom Domain (Optional)

1. Go to **Site Settings** → **Domain Management**
2. Click **Add custom domain**
3. Enter your domain (e.g., `app.yourdomain.com`)
4. Follow DNS configuration instructions (CNAME or A records)
5. Wait for DNS propagation (can take 5-15 minutes)

### Step 6: Set Up SSL Certificate

Netlify automatically provisions SSL certificates (HTTPS) within 24 hours. Check status:
1. **Site Settings** → **Domain Management**
2. Look for "SSL certificate" status

---

## Deployment Contexts

### Production Context
- **Branch**: `main`
- **Command**: `npm ci && npm run build`
- **Environment**: `VITE_ENVIRONMENT=production`
- **API URL**: `https://api.yourdomain.com`

### Staging Context
- **Branch**: `staging` (if you create one)
- **Command**: `npm ci && npm run build:staging`
- **Environment**: `VITE_ENVIRONMENT=staging`
- **API URL**: `https://api-staging.yourdomain.com`
- **Automatic**: Branch-deploy preview at unique URL

### Preview Context
- **Trigger**: Pull requests
- **Command**: `npm ci && npm run build:preview`
- **Environment**: `VITE_ENVIRONMENT=development`
- **Automatic**: Creates preview URL for each PR

---

## Build & Deploy Monitoring

### View Build Logs

1. Go to **Deploys**
2. Click on any deployment
3. Click **View full logs** to see build output

### Example Successful Build Output:

```
> real-estate-wholesale-platform-frontend@1.0.0 build
> vite build

✓ built in 45.23s

Output file size analysis:
  dist/index.html                                0.55 kB
  dist/js/vendor-a1b2c3d4.js                   125.45 kB
  dist/js/app-e5f6g7h8.js                       85.30 kB
  dist/assets/main-i9j0k1l2.css                 32.15 kB
```

### Troubleshooting Common Build Errors

#### Error: "npm: command not found"
- Netlify Node version may not match
- Solution: Add to netlify.toml:
  ```
  [build.environment]
    NODE_VERSION = "18.17.0"
  ```

#### Error: "Cannot find module 'vue'"
- Dependencies not installed
- Ensure `frontend/package.json` exists
- Check build command is: `npm ci && npm run build`

#### Error: "ENOENT: no such file or directory, open 'dist'"
- Vite not building to correct directory
- Check `vite.config.js` has: `outDir: 'dist'`

---

## Performance Optimization

The `netlify.toml` includes optimizations:

1. **Code Splitting**: Vendor code separated from app code
2. **Asset Versioning**: Files include hash for cache busting
3. **Cache Headers**: Long-lived caching for immutable assets
4. **Compression**: Gzip compression enabled automatically
5. **CDN Caching**: Content distributed globally

---

## Security Configuration

Netlify.toml includes security headers:

- **X-Content-Type-Options**: Prevents MIME type sniffing
- **X-Frame-Options**: Prevents clickjacking
- **X-XSS-Protection**: Enables browser XSS filters
- **Referrer-Policy**: Controls referrer information

---

## Connecting Backend API

The frontend is configured to proxy API calls to your backend:

### Frontend API Configuration
```javascript
// In vite.config.js
proxy: {
  '/api': {
    target: process.env.VITE_API_BASE_URL || 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

### Backend Requirements
1. Deploy backend to separate service (AWS, GCP, Azure, etc.)
2. Set `VITE_API_BASE_URL` to backend URL
3. Enable CORS on backend for Netlify domain
4. Example: `VITE_API_BASE_URL=https://api.yourdomain.com`

---

## Advanced Configuration

### Custom Redirects
Edit `netlify.toml` `[[redirects]]` section to add:
```toml
[[redirects]]
  from = "/old-path/*"
  to = "/new-path/:splat"
  status = 301
```

### Add serverless functions
Place functions in `netlify/functions/` directory:
```javascript
// netlify/functions/submit-lead.js
exports.handler = async (event) => {
  // Lambda function code
  return { statusCode: 200, body: 'Success' };
};
```

### Monorepo Support
If using monorepo (multiple packages):
```toml
[build]
  command = "npm ci --workspaces && npm run build"
  base = "packages/frontend"
```

---

## Summary: Build Settings Configuration

Copy these settings exactly into Netlify UI:

**Site Settings → Build & Deploy → Build Settings**
```
Branch to deploy:           main
Base directory:             frontend
Build command:              npm ci && npm run build
Publish directory:          dist
Functions directory:        netlify/functions
```

**Environment Variables** (Add via Site Settings → Environment):
```
VITE_API_BASE_URL           https://api.yourdomain.com
VITE_ENVIRONMENT            production
```

**Once configured:**
1. Every push to `main` triggers automatic build
2. Build logs show in Netlify Dashboard
3. Successful build deploys to your domain
4. Failed builds send notifications (configurable)

---

## Monitoring & Analytics

After deployment:

1. **Netlify Analytics**: **Analytics** tab shows traffic
2. **Build Analytics**: **Deploys** → deployment → scroll for build time
3. **Function Logs**: **Functions** → invoke → view real-time logs

---

## Next Steps

1. ✅ Push this repository to GitHub
2. ✅ Connect GitHub to Netlify (Steps 2-3 above)
3. ✅ Configure environment variables (Step 4)
4. ✅ Set up custom domain (Step 5)
5. ✅ Deploy backend API separately
6. ✅ Test full platform at `https://yourdomain.com`

Your platform is now ready for global deployment! 🚀
