# Deployment Guide: Phishing Simulation System

## Deploy to PythonAnywhere (Free Tier)

### 1. Sign Up
- Go to https://www.pythonanywhere.com/
- Create a free account

### 2. Upload Your Files
**Option A: Using Git (Recommended)**
```bash
# On PythonAnywhere Bash console:
git clone https://github.com/yourusername/phishing-sim.git
cd phishing-sim
```

**Option B: Upload via Files tab**
- Use PythonAnywhere's Files interface
- Upload all files from your project

### 3. Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 phishing-sim
pip install -r requirements.txt
```

### 4. Configure Web App
1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration** → **Python 3.10**
4. Set source code directory: `/home/yourusername/phishing-sim`
5. Set working directory: `/home/yourusername/phishing-sim`

### 5. Edit WSGI Configuration File
Click on the WSGI configuration file link and replace content with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/phishing-sim'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key-here'

# Import your Flask app
from app import app as application
```

### 6. Set Up Database
- SQLite database will be created automatically at `/home/yourusername/phishing-sim/phishing_sim.db`
- Make sure the directory is writable

### 7. Configure Custom Domain
**A. In PythonAnywhere (Free accounts limited):**
- Free accounts get: `yourusername.pythonanywhere.com`
- Paid accounts can use custom domains

**B. For Custom Domain (Requires Paid Account):**
1. In Web tab, add `phishing-test.fwh.is` to allowed domains
2. In your domain DNS (fwh.is provider):
   - Add CNAME record: `phishing-test` → `yourusername.pythonanywhere.com`
   - Or A record pointing to PythonAnywhere's IP

**C. Update your app.py:**
```python
# Change the base URL in campaign creation to:
# https://phishing-test.fwh.is or https://yourusername.pythonanywhere.com
```

### 8. Reload Web App
- Click **Reload [yourusername].pythonanywhere.com** button
- Visit your site!

---

## Alternative: Deploy to Render.com (Easier, Custom Domain on Free Tier)

### 1. Sign Up
- Go to https://render.com
- Sign up with GitHub

### 2. Create render.yaml (add to your project)
```yaml
services:
  - type: web
    name: phishing-sim
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: SECRET_KEY
        generateValue: true
```

### 3. Update app.py for Production
Change the last line from:
```python
app.run(host="0.0.0.0", port=5000, debug=False)
```
To:
```python
port = int(os.getenv("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=False)
```

### 4. Deploy
1. Push code to GitHub
2. Connect repository in Render dashboard
3. Render auto-deploys
4. Add custom domain `phishing-test.fwh.is` in settings

### 5. DNS Configuration
In your domain provider (fwh.is):
- Add CNAME record: `phishing-test` → `your-app.onrender.com`

---

## Important Security Notes

⚠️ **Before deploying:**

1. **Change SECRET_KEY** in production:
   ```python
   app.secret_key = os.getenv("SECRET_KEY", "change-this-in-production")
   ```
   Set a strong random key as environment variable

2. **Use HTTPS only** for production (both platforms provide free SSL)

3. **Add authentication** to admin routes (currently public!)

4. **Get proper authorization** from your organization before deploying

5. **Backup database regularly**

6. **Monitor email sending limits** (Gmail: 500/day with App Password)

---

## Quick Comparison

| Platform | Python Support | Free Tier | Custom Domain | SSL | Best For |
|----------|----------------|-----------|---------------|-----|----------|
| InfinityFree | ❌ PHP only | ✅ | ✅ | ✅ | Not suitable |
| PythonAnywhere | ✅ | ✅ | 💰 Paid only | ✅ | Learning/Testing |
| Render | ✅ | ✅ | ✅ Free | ✅ | **Recommended** |
| Railway | ✅ | ✅ | ✅ Free | ✅ | Good option |
| Heroku | ✅ | ❌ Paid | ✅ | ✅ | Paid option |

## Recommendation

**Use Render.com** - it offers the best balance of:
- Free hosting with Python support
- Custom domain support (free)
- Automatic SSL/HTTPS
- Easy deployment from GitHub
- Good free tier limits
