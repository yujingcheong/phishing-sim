# 🎣 Phishing Simulation System

A professional phishing awareness training tool for security testing and employee education.

## ⚠️ Important Legal Notice

**This tool is for AUTHORIZED INTERNAL SECURITY TESTING ONLY.**

- ✅ Use only with explicit written authorization from your organization
- ✅ For employee security awareness training purposes
- ✅ For internal audit preparation
- ❌ DO NOT use for unauthorized testing
- ❌ DO NOT use for malicious purposes

## 🎯 Features

- **4 Pre-built Phishing Templates**
  - IT Password Reset
  - HR Payroll Update
  - CEO Urgent Request
  - Shared File Notification

- **Real-time Tracking**
  - Email sent tracking
  - Click tracking with IP & user agent
  - Credential submission tracking
  - Reporting functionality

- **Analytics Dashboard**
  - Click rates
  - Submission rates
  - Department analysis
  - CSV export for reports

- **Educational Landing Pages**
  - Immediate user awareness feedback
  - Security tips after click
  - No actual credential storage

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/phishing-sim.git
   cd phishing-sim
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the dashboard**
   - Open: http://localhost:5000

### Deploy to Production

See [RENDER_DEPLOY_GUIDE.md](RENDER_DEPLOY_GUIDE.md) for complete deployment instructions to Render.com.

## 📊 Usage

### 1. Create Campaign
- Choose a phishing template
- Add target employees (CSV format: email, name, department)
- Configure SMTP settings (Gmail App Password required)
- Set tracking base URL

### 2. Launch Campaign
- System sends phishing emails
- Tracks who clicks the link
- Records credential submissions
- Shows awareness page after submission

### 3. View Results
- Dashboard shows real-time statistics
- Export detailed CSV reports
- Analyze departmental vulnerabilities

## 🔧 Configuration

### Gmail SMTP Setup

1. Enable 2-Factor Authentication on Gmail
2. Generate App Password at: https://myaccount.google.com/apppasswords
3. Use the 16-character App Password (NOT your Gmail password)

### Environment Variables

Create a `.env` file:
```
SECRET_KEY=your-secret-key-here
```

## 📁 Project Structure

```
phishing-sim/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── render.yaml               # Render.com deployment config
├── RENDER_DEPLOY_GUIDE.md    # Deployment guide
├── templates/                # (Auto-generated at runtime)
├── static/                   # (Auto-generated at runtime)
└── instance/                 # SQLite database folder
    └── phishing_sim.db       # Database file
```

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Email:** SMTP (Gmail compatible)
- **Deployment:** Render.com / PythonAnywhere / Railway

## 📋 Requirements

- Python 3.10+
- Flask 2.3+
- SQLAlchemy 2.0+
- Valid SMTP server credentials

## 🔐 Security Considerations

### What This Tool Does:
✅ Educates employees about phishing  
✅ Tests organizational vulnerability  
✅ Provides awareness training  
✅ Generates compliance reports  

### What This Tool Does NOT Do:
❌ Store actual credentials  
❌ Perform malicious actions  
❌ Violate privacy laws  
❌ Bypass authorization  

### Before Deployment:
1. ⚠️ Get written authorization from management
2. ⚠️ Inform legal/HR departments
3. ⚠️ Add authentication to admin routes
4. ⚠️ Use strong `SECRET_KEY`
5. ⚠️ Enable HTTPS in production
6. ⚠️ Follow your organization's policies

## 📜 License

This project is for educational and authorized security training purposes only.

**Use responsibly and ethically.**

## 🤝 Contributing

This is an internal security tool. Ensure all contributions maintain ethical standards and legal compliance.

## 📞 Support

For deployment help, see:
- [RENDER_DEPLOY_GUIDE.md](RENDER_DEPLOY_GUIDE.md) - Render.com deployment
- [DEPLOYMENT.md](DEPLOYMENT.md) - Alternative platforms

## ⚖️ Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. Use of this software for unauthorized testing or malicious purposes is strictly prohibited and may be illegal. Users are solely responsible for compliance with applicable laws and regulations.

---

**Built for internal security awareness training • Use responsibly • Get authorization first**
