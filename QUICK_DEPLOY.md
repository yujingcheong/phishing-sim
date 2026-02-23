# Quick Deployment to Render.com (Recommended)

Your domain: `https://phishing-test.fwh.is/`

## Why Not InfinityFree?
❌ **InfinityFree only supports PHP**, not Python/Flask. You need Python hosting.

## Deploy to Render.com (FREE with Custom Domain)

### Step 1: Push to GitHub (If Not Already)
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/phishing-sim.git
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: `phishing-sim`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Click **"Create Web Service"**

Render will auto-deploy! You'll get a URL like: `https://phishing-sim.onrender.com`

### Step 3: Add Your Custom Domain
1. In Render dashboard, go to your service
2. Click **"Settings"** → **"Custom Domain"**
3. Add: `phishing-test.fwh.is`
4. Render will show you DNS records to add

### Step 4: Configure DNS at FWH.is
Go to your domain provider (freenom/freewebhosting) and add:

**CNAME Record:**
- Name: `phishing-test` (or `@` if using root domain)
- Value: `phishing-sim.onrender.com`
- TTL: 3600

Wait 5-60 minutes for DNS propagation.

### Step 5: Test
Visit: https://phishing-test.fwh.is/

✅ You're live!

---

## Important: Update Base URL in Campaigns

When creating campaigns, use your domain as the base URL:
```
https://phishing-test.fwh.is
```

---

## Environment Variables (Security)

In Render dashboard, add environment variables:
- `SECRET_KEY`: Generate a random string (Render can auto-generate)

---

## Free Tier Limits (Render)
- ✅ 750 hours/month (enough for always-on)
- ✅ Custom domain with SSL
- ⚠️ May sleep after 15 min of inactivity (first request takes ~30s to wake)

---

## Alternative: PythonAnywhere

If Render doesn't work, see DEPLOYMENT.md for PythonAnywhere instructions.
