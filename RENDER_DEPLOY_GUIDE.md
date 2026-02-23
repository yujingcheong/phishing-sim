# 🚀 Deploy Your Phishing Sim to Render.com

**Complete Step-by-Step Guide for Malaysian Developers**

Your domain: `https://phishing-test.fwh.is/`

---

## ✅ Prerequisites Checklist

Before you start:
- [ ] Have a GitHub account (free)
- [ ] Have a Render.com account (free, no credit card needed)
- [ ] Your Gmail App Password ready
- [ ] Your code is ready on your computer

---

## 📋 Step 1: Push Your Code to GitHub

### Option A: Using GitHub Desktop (Easiest)

1. **Download & Install GitHub Desktop**
   - Go to: https://desktop.github.com/
   - Install and sign in

2. **Create New Repository**
   - File → Add Local Repository → Choose `C:\Users\abc\phishing-sim`
   - If it says "not a git repository", click "Create Repository"
   - Repository name: `phishing-sim`
   - Click "Create Repository"

3. **Publish to GitHub**
   - Click "Publish repository" (top right)
   - Uncheck "Keep this code private" OR keep it private (both work)
   - Click "Publish repository"

✅ Done! Your code is now on GitHub.

### Option B: Using Command Line

```powershell
cd C:\Users\abc\phishing-sim

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Phishing Simulation System"

# Create GitHub repo and push
# (You'll need to create the repo on GitHub.com first, then:)
git remote add origin https://github.com/YOUR-USERNAME/phishing-sim.git
git branch -M main
git push -u origin main
```

---

## 🌐 Step 2: Deploy to Render.com

### 2.1 Sign Up for Render

1. Go to: **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. **Sign up with GitHub** (recommended - easiest)
4. Authorize Render to access your GitHub

### 2.2 Create New Web Service

1. Click **"New +"** (top right) → **"Web Service"**

2. **Connect Your Repository**
   - You'll see a list of your GitHub repos
   - Find and click **"Connect"** next to `phishing-sim`
   - (If you don't see it, click "Configure account" to give Render access)

3. **Configure the Service**
   Fill in these settings:

   | Field | Value |
   |-------|-------|
   | **Name** | `phishing-sim` (or any name you like) |
   | **Region** | `Singapore` (closest to Malaysia!) |
   | **Branch** | `main` |
   | **Root Directory** | (leave blank) |
   | **Environment** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |
   | **Instance Type** | `Free` |

4. **Click "Create Web Service"**

✅ Render will now:
- Build your app (~2-3 minutes)
- Deploy it automatically
- Give you a URL like: `https://phishing-sim.onrender.com`

**Wait for the build to complete** - you'll see logs scrolling. Wait for "Build successful" message.

---

## 🔧 Step 3: Add Environment Variables (Optional but Recommended)

While the build is running or after:

1. Go to your service dashboard on Render
2. Click **"Environment"** tab (left sidebar)
3. Click **"Add Environment Variable"**
4. Add:
   - **Key:** `SECRET_KEY`
   - **Value:** Click "Generate" or type a random string
5. Click **"Save Changes"**

This will auto-redeploy with the new variable.

---

## 🌍 Step 4: Connect Your Custom Domain

### 4.1 In Render Dashboard

1. Go to your service on Render
2. Click **"Settings"** tab
3. Scroll to **"Custom Domain"**
4. Click **"Add Custom Domain"**
5. Enter: `phishing-test.fwh.is`
6. Click **"Save"**

Render will show you DNS records to add (usually a CNAME).

### 4.2 Configure DNS at Your Domain Provider

Go to where you registered `fwh.is` (Freenom, etc.):

**Add CNAME Record:**
```
Type: CNAME
Name: phishing-test (or @ for root domain)
Value: phishing-sim.onrender.com
TTL: 3600
```

**Save the DNS record.**

⏰ **Wait 5-60 minutes** for DNS to propagate globally.

---

## ✅ Step 5: Test Your Deployment

### 5.1 Test the Render URL

1. Visit: `https://phishing-sim.onrender.com`
2. You should see your dashboard!

### 5.2 Test Your Custom Domain

After DNS propagates:
1. Visit: `https://phishing-test.fwh.is`
2. Should work the same!

### 5.3 Create Your First Campaign

1. Click **"New Campaign"**
2. Fill in the form:
   - **Campaign Name:** "Test Campaign"
   - **Template:** Any template
   - **Targets:**
     ```
     yujingcheong@gmail.com,Yu Jing,IT
     jianfenggamingacc@gmail.com,Jeff,IT
     ```
   - **Sender Email:** Your Gmail address
   - **SMTP Server:** `smtp.gmail.com`
   - **SMTP Port:** `587`
   - **SMTP Username:** Your full Gmail address
   - **SMTP Password:** Your 16-character App Password (without spaces!)
   - **Tracking Base URL:** `https://phishing-test.fwh.is`

3. Click **"Launch Campaign"**

✅ Emails should be sent!

---

## 📊 Step 6: Monitor Your App

### View Logs on Render

1. Go to your service dashboard
2. Click **"Logs"** tab
3. See real-time logs

### Check if App is Sleeping

⚠️ **Free tier:** Apps sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Subsequent requests are instant

To keep it awake, use a service like:
- **UptimeRobot** (https://uptimerobot.com) - free pings every 5 minutes
- Set it to ping: `https://phishing-test.fwh.is`

---

## 🔄 Step 7: Update Your App Later

When you make changes:

1. **Edit code on your computer**
2. **Commit and push to GitHub:**
   ```powershell
   git add .
   git commit -m "Update feature"
   git push
   ```
3. **Render auto-deploys** in ~2 minutes!

---

## ⚠️ Important Notes

### Security

✅ **HTTPS is automatic** - Render provides free SSL  
✅ Change `SECRET_KEY` in environment variables  
⚠️ Add authentication to admin routes before real use  
⚠️ Get proper authorization before deploying  

### Gmail Limits

📧 Gmail App Password limit: **500 emails per day**  
📧 For more, use SendGrid, Mailgun, or AWS SES  

### Free Tier Limits (Render)

✅ 750 hours/month (enough for 24/7)  
✅ Custom domain with SSL  
⚠️ Sleeps after 15 min inactivity  
⚠️ 512 MB RAM  
⚠️ Shared CPU  

---

## 🐛 Troubleshooting

### "Build Failed"
- Check logs tab for errors
- Make sure `requirements.txt` is correct
- Check `render.yaml` syntax

### "Application Error"
- Check logs for Python errors
- Verify `gunicorn` is in requirements.txt
- Check start command

### SMTP Errors
- Use Gmail App Password, NOT regular password
- Generate at: https://myaccount.google.com/apppasswords
- Enter 16 characters without spaces

### Domain Not Working
- Wait up to 1 hour for DNS propagation
- Check DNS settings are correct
- Clear browser cache

### App is Slow
- Free tier sleeps after 15 min
- First request takes ~30 seconds
- Use UptimeRobot to keep awake

---

## 🎉 You're Done!

Your phishing simulation system is now:

✅ Live at `https://phishing-test.fwh.is`  
✅ Auto-deployed from GitHub  
✅ HTTPS/SSL enabled  
✅ Ready to test!

**Need help?** Check Render docs: https://render.com/docs

---

## 📝 Quick Commands Reference

```powershell
# Update code
git add .
git commit -m "Your update message"
git push

# View local changes
git status

# Restart app on Render
# Go to dashboard → Manual Deploy → "Clear build cache & deploy"
```

---

**Happy testing! 🎣**
