# Netlify Build Settings - Exact Configuration Values

This document provides the exact values to enter in Netlify's build configuration interface.

## Location in Netlify UI

**Netlify Dashboard** → **Site Settings** → **Build & Deploy** → **Build Settings**

---

## Field-by-Field Configuration

### 1. Branch to deploy

**Field Label**: "Branch to deploy"  
**Value to Enter**: `main`  
**Alternative**: `master` (if that's your default branch)

**How to set**:
1. In Netlify Dashboard, go to **Build & Deploy**
2. Look for "Continuous Deployment" section
3. Check the **Branches** setting
4. Should show: "Deploy only on push to these branches"
5. Enter: `main`

---

### 2. Base directory

**Field Label**: "Base directory" (also called "Base directory")  
**Description**: "The directory where Netlify installs dependencies and runs your build command"  
**Value to Enter**: `frontend`

**Explanation**: 
- This is where your `package.json` is located
- Netlify will `cd` into this directory before running build
- All build commands execute from here

**How to set**:
1. Dashboard → **Build & Deploy** → **Build Settings**
2. Click **Edit settings**
3. In "Base directory" field, type: `frontend`
4. Click **Save**

---

### 3. Build command

**Field Label**: "Build command"  
**Description**: "Examples: jekyll build, gulp build, make all"  
**Value to Enter**: `npm ci && npm run build`

**Explanation**:
- `npm ci` = Clean install from package-lock.json (reproducible, CI-optimized)
- `&&` = Run next command only if first succeeds
- `npm run build` = Execute the "build" script from package.json

**What this does**:
1. Installs exact dependency versions (30-45 seconds)
2. Compiles Vue/TypeScript with Vite (15-30 seconds)
3. Creates optimized output in `dist/` folder

**Total build time**: 45-75 seconds

**How to set**:
1. Dashboard → **Build & Deploy** → **Build Settings**
2. Click **Edit settings**
3. In "Build command" field, type: `npm ci && npm run build`
4. Click **Save**

---

### 4. Publish directory

**Field Label**: "Publish directory"  
**Description**: "Examples: _site, dist, public"  
**Value to Enter**: `dist`

**Explanation**:
- This is the folder that gets deployed to the internet
- Vite outputs the built React app here
- Netlify serves this folder's contents on your domain

**What's in `dist/`**:
- `index.html` - Main HTML file
- `js/*.js` - JavaScript bundles
- `assets/*` - CSS, images, fonts
- `netlify.toml` - Netlify configuration (referenced)

**How to set**:
1. Dashboard → **Build & Deploy** → **Build Settings**
2. Click **Edit settings**
3. In "Publish directory" field, type: `dist`
4. Click **Save**

---

### 5. Functions directory

**Field Label**: "Functions directory"  
**Description**: "netlify/functions"  
**Value to Enter**: `netlify/functions`

**Explanation**:
- Optional: For serverless functions
- Place any Lambda-like functions here
- Can be left as default for now
- Create this folder if you add serverless functions later

**Current status**: No functions currently in project (can add later)

**How to set**:
1. Dashboard → **Build & Deploy** → **Build Settings**
2. Click **Edit settings**
3. In "Functions directory" field, type: `netlify/functions`
4. Click **Save**

---

## Environment Variables Configuration

**Location**: **Site Settings** → **Build & Deploy** → **Environment** → **Edit variables**

### Required Environment Variables

Add these variables one by one:

#### Variable 1: API Base URL

| Key | Value |
|-----|-------|
| `VITE_API_BASE_URL` | `https://api.yourdomain.com` |

**Instructions**:
1. In "Key" field: type `VITE_API_BASE_URL`
2. In "Value" field: type `https://api.yourdomain.com`
   - Replace `yourdomain.com` with your actual domain
   - Example: `https://api.realestatefastrack.com`
3. Click "Add"

#### Variable 2: Environment

| Key | Value |
|-----|-------|
| `VITE_ENVIRONMENT` | `production` |

**Instructions**:
1. In "Key" field: type `VITE_ENVIRONMENT`
2. In "Value" field: type `production`
3. Click "Add"

### Optional Environment Variables

#### Variable 3: Sentry Error Tracking (Optional)

| Key | Value |
|-----|-------|
| `VITE_SENTRY_DSN` | `https://[key]@sentry.io/[project-id]` |

**Instructions** (only if using Sentry):
1. Sign up at https://sentry.io
2. Create a project
3. Get your DSN (looks like: `https://abc123xyz@sentry.io/999999`)
4. In Netlify → "Key" field: type `VITE_SENTRY_DSN`
5. In "Value" field: paste your DSN
6. Click "Add"

#### Variable 4: Google Analytics (Optional)

| Key | Value |
|-----|-------|
| `VITE_GA_TRACKING_ID` | `UA-XXXXXXXXX-X` |

**Instructions** (only if using Google Analytics):
1. Set up account at https://analytics.google.com
2. Get your Tracking ID (looks like: `UA-1234567-1`)
3. In Netlify → "Key" field: type `VITE_GA_TRACKING_ID`
4. In "Value" field: paste your ID
5. Click "Add"

### Feature Flag Variables (Optional)

These control which features appear in the UI:

**Variable**: Feature Flags

| Key | Value |
|-----|-------|
| `VITE_ENABLE_LEAD_SCOUT` | `true` |
| `VITE_ENABLE_OFFER_GENERATOR` | `true` |
| `VITE_ENABLE_BUYER_MATCHER` | `true` |
| `VITE_ENABLE_NEGOTIATION_ASSISTANT` | `true` |
| `VITE_ENABLE_SEO_CONTENT` | `true` |

**Instructions** (to control features):
1. For each flag above, add as separate variable
2. Set value to `true` to enable or `false` to disable
3. Example:
   - Key: `VITE_ENABLE_LEAD_SCOUT`
   - Value: `true`
   - Click "Add"

---

## Complete Example Configuration

### Build Settings Tab

```
Branch to deploy:        main
Base directory:          frontend
Build command:           npm ci && npm run build
Publish directory:       dist
Functions directory:     netlify/functions
```

### Environment Variables Tab

```
VITE_API_BASE_URL        https://api.yourdomain.com
VITE_ENVIRONMENT         production
VITE_ENABLE_LEAD_SCOUT   true
VITE_ENABLE_OFFER_GENERATOR  true
VITE_ENABLE_BUYER_MATCHER    true
VITE_ENABLE_NEGOTIATION_ASSISTANT  true
VITE_ENABLE_SEO_CONTENT  true
```

---

## Order of Configuration Steps

1. **First**: Push code to GitHub
2. **Second**: Connect repository to Netlify
3. **Third**: Verify build settings (should auto-fill from netlify.toml)
4. **Fourth**: Add environment variables
5. **Fifth**: Click "Deploy site"
6. **Sixth**: Monitor build in Deploys tab
7. **Seventh**: Test at preview URL

---

## Expected Build Output

After clicking "Deploy site", you should see in the build logs:

```
> npm ci
added 250 packages in 45s

> npm run build
✓ 1243 modules transformed
✓ built in 28.32s
```

Then Netlify will:
1. Deploy `dist/` folder to CDN
2. Create preview URL: `https://xxxxx.netlify.app`
3. Apply redirects and headers from netlify.toml
4. Make site live at your domain (if connected)

---

## Verification Checklist

After entering all values:

- [ ] "Branch to deploy" = `main`
- [ ] "Base directory" = `frontend`
- [ ] "Build command" = `npm ci && npm run build`
- [ ] "Publish directory" = `dist`
- [ ] "Functions directory" = `netlify/functions`

Environment Variables set:
- [ ] `VITE_API_BASE_URL` = `https://api.yourdomain.com`
- [ ] `VITE_ENVIRONMENT` = `production`
- [ ] Feature flags = `true` (or `false` if disabling)

Optional variables (if applicable):
- [ ] `VITE_SENTRY_DSN` (if using Sentry)
- [ ] `VITE_GA_TRACKING_ID` (if using Google Analytics)

---

## Common Configuration Errors

### ❌ Wrong Base Directory
- **DON'T**: leave blank or put `/`
- **DON'T**: use `./frontend` (Netlify expects relative paths)
- **DO**: type `frontend`

### ❌ Wrong Build Command
- **DON'T**: use `npm install && npm run build` (slower, less reliable)
- **DON'T**: use `npm build` (npm doesn't have this command)
- **DO**: use `npm ci && npm run build`

### ❌ Wrong Publish Directory
- **DON'T**: use `frontend/dist` (use relative path: `dist`)
- **DON'T**: use `./dist` (Netlify expects `dist`)
- **DO**: use `dist`

### ❌ Wrong API URL
- **DON'T**: use `localhost:8000` (won't work in production)
- **DON'T**: use `http://api.yourdomain.com` (should be HTTPS)
- **DO**: use `https://api.yourdomain.com`

---

## Support & Troubleshooting

**If build fails**:
1. Dashboard → **Deploys** → latest deploy
2. Click **View full logs**
3. Read error messages (usually near bottom)
4. Check NETLIFY_CHECKLIST.md for solutions

**If site won't load**:
1. Check preview URL works: `https://xxxxx.netlify.app`
2. Check custom domain DNS: added CNAME record?
3. Check HTTPS certificate: provisioned within 24 hours?

**If API calls fail**:
1. Verify `VITE_API_BASE_URL` is correct
2. Check backend API is deployed and running
3. Check backend has CORS enabled for your domain
4. Open DevTools (F12) → Network tab → inspect API request

---

## Quick Copy-Paste References

### For Build Settings

```
main
frontend
npm ci && npm run build
dist
netlify/functions
```

### For Environment Variables (minimum)

```
VITE_API_BASE_URL     https://api.yourdomain.com
VITE_ENVIRONMENT      production
```

### For Environment Variables (complete)

```
VITE_API_BASE_URL            https://api.yourdomain.com
VITE_ENVIRONMENT             production
VITE_ENABLE_LEAD_SCOUT       true
VITE_ENABLE_OFFER_GENERATOR  true
VITE_ENABLE_BUYER_MATCHER    true
VITE_ENABLE_NEGOTIATION_ASSISTANT  true
VITE_ENABLE_SEO_CONTENT      true
```

---

## Next Action

1. Open https://app.netlify.com
2. Connect your GitHub repository
3. Enter these build settings exactly as shown above
4. Set environment variables from the "Complete Example" section
5. Click "Deploy site"
6. Watch build logs in Dashboard → Deploys tab
7. Test at the preview URL

**You're ready to launch!** 🚀
