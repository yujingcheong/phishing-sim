# 📋 Deployment Checklist

Use this checklist to deploy your app to Render.com!

## Pre-Deployment ✅

- [ ] Gmail App Password generated (https://myaccount.google.com/apppasswords)
- [ ] GitHub account created (https://github.com)
- [ ] Render.com account created (https://render.com)
- [ ] All code tested locally

## Step 1: Push to GitHub ✅

- [ ] Installed Git or GitHub Desktop
- [ ] Created repository on GitHub (name: `phishing-sim`)
- [ ] Pushed all code to GitHub
- [ ] Verified code appears on GitHub.com

## Step 2: Deploy to Render ✅

- [ ] Signed up for Render with GitHub
- [ ] Created new Web Service
- [ ] Connected `phishing-sim` repository
- [ ] Configured settings:
  - [ ] Name: `phishing-sim`
  - [ ] Region: `Singapore`
  - [ ] Environment: `Python 3`
  - [ ] Build command: `pip install -r requirements.txt`
  - [ ] Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
  - [ ] Instance type: `Free`
- [ ] Clicked "Create Web Service"
- [ ] Waited for build to complete (~2-3 minutes)
- [ ] Build shows "Live" status

## Step 3: Test Render URL ✅

- [ ] Visited: `https://phishing-sim.onrender.com` (or your service URL)
- [ ] Dashboard loads successfully
- [ ] No errors in browser console

## Step 4: Add Custom Domain ✅

- [ ] In Render Settings → Custom Domain
- [ ] Added domain: `phishing-test.fwh.is`
- [ ] Copied CNAME record value
- [ ] Added CNAME in domain DNS settings:
  ```
  Type: CNAME
  Name: phishing-test
  Value: phishing-sim.onrender.com
  TTL: 3600
  ```
- [ ] Saved DNS settings
- [ ] Waited 30-60 minutes for DNS propagation
- [ ] Tested custom domain: `https://phishing-test.fwh.is`

## Step 5: Configure Environment Variables ✅

- [ ] In Render → Environment tab
- [ ] Added `SECRET_KEY`:
  - [ ] Key: `SECRET_KEY`
  - [ ] Value: (Generated or random string)
- [ ] Saved changes
- [ ] App redeployed automatically

## Step 6: Test Campaign ✅

- [ ] Visited dashboard
- [ ] Clicked "New Campaign"
- [ ] Filled in test campaign:
  - [ ] Campaign name entered
  - [ ] Template selected
  - [ ] Test email addresses added
  - [ ] Gmail address as sender
  - [ ] SMTP settings configured:
    - [ ] Server: `smtp.gmail.com`
    - [ ] Port: `587`
    - [ ] Username: Full Gmail address
    - [ ] Password: 16-char App Password (NO SPACES!)
  - [ ] Base URL: `https://phishing-test.fwh.is`
- [ ] Clicked "Launch Campaign"
- [ ] Campaign launched successfully
- [ ] Checked target inbox for email
- [ ] Tested clicking phishing link
- [ ] Verified tracking works
- [ ] Checked dashboard for results

## Optional: Keep App Awake ✅

- [ ] Signed up for UptimeRobot (https://uptimerobot.com)
- [ ] Created monitor for: `https://phishing-test.fwh.is`
- [ ] Set interval: 5 minutes
- [ ] App stays awake (no 30-second delay)

## Final Verification ✅

- [ ] Dashboard accessible
- [ ] HTTPS working (🔒 in browser)
- [ ] Custom domain working
- [ ] SMTP sending emails
- [ ] Click tracking working
- [ ] Reports downloadable
- [ ] No errors in Render logs

---

## 🎉 Deployment Complete!

Your app is live at:
- ✅ `https://phishing-test.fwh.is`
- ✅ `https://phishing-sim.onrender.com`

---

## 🐛 If Something Went Wrong:

### Build Failed
- [ ] Checked Render logs for errors
- [ ] Verified `requirements.txt` is correct
- [ ] Retried build with "Clear build cache & deploy"

### App Error
- [ ] Checked Render logs tab
- [ ] Verified start command is correct
- [ ] Checked environment variables

### SMTP Not Working
- [ ] Using Gmail App Password (NOT regular password)
- [ ] App Password has no spaces
- [ ] Used full email address as username

### Domain Not Working
- [ ] Waited at least 30 minutes
- [ ] Checked DNS settings are correct
- [ ] Cleared browser cache
- [ ] Tried incognito/private browsing

---

**Need help?** See [RENDER_DEPLOY_GUIDE.md](RENDER_DEPLOY_GUIDE.md) for detailed troubleshooting.
