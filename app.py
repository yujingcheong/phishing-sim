"""
Phishing Simulation System - Employee Security Awareness Testing
For internal audit preparation and security training purposes only.
"""

import os
import uuid
import smtplib
import csv
import json
import threading
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, redirect, render_template_string, jsonify, session
from sqlalchemy.orm import joinedload
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///phishing_sim.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

_db_initialised = False

@app.before_request
def init_db():
    global _db_initialised
    if not _db_initialised:
        db.create_all()
        _db_initialised = True

# ─────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────

class Campaign(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)
    template    = db.Column(db.String(50), nullable=False)   # e.g. "it_password_reset"
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    targets     = db.relationship("Target", backref="campaign", lazy=True)

class Target(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"), nullable=False)
    email       = db.Column(db.String(200), nullable=False)
    name        = db.Column(db.String(200))
    department  = db.Column(db.String(100))
    token       = db.Column(db.String(64), unique=True, default=lambda: uuid.uuid4().hex)
    sent_at     = db.Column(db.DateTime)
    clicked_at  = db.Column(db.DateTime)
    submitted_at= db.Column(db.DateTime)
    ip_address  = db.Column(db.String(50))
    user_agent  = db.Column(db.String(500))
    reported    = db.Column(db.Boolean, default=False)  # did employee report it?

# ─────────────────────────────────────────────
# EMAIL TEMPLATES (simulated phishing scenarios)
# ─────────────────────────────────────────────

EMAIL_TEMPLATES = {
    "it_password_reset": {
        "subject": "⚠️ Action Required: Your password will expire in 24 hours",
        "sender_name": "IT Help Desk",
        "body_html": """
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #ddd;padding:24px">
          <h2 style="color:#c0392b">IT Security Alert</h2>
          <p>Dear {name},</p>
          <p>Your account password is set to expire in <strong>24 hours</strong>. To avoid losing access to company systems, please reset your password immediately.</p>
          <p style="text-align:center">
            <a href="{link}" style="background:#c0392b;color:white;padding:12px 24px;text-decoration:none;border-radius:4px;display:inline-block">
              Reset My Password Now
            </a>
          </p>
          <p style="color:#888;font-size:12px">If you did not request this, please contact IT support immediately.</p>
          <p style="color:#888;font-size:12px">IT Help Desk | Your Company</p>
        </div>
        """,
    },
    "hr_payroll_update": {
        "subject": "Important: Update your payroll direct deposit information",
        "sender_name": "HR Department",
        "body_html": """
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #ddd;padding:24px">
          <h2 style="color:#2980b9">HR Payroll Update Required</h2>
          <p>Dear {name},</p>
          <p>As part of our annual payroll system upgrade, all employees must verify their direct deposit information by <strong>end of this week</strong>.</p>
          <p>Failure to update may result in delayed salary payments.</p>
          <p style="text-align:center">
            <a href="{link}" style="background:#2980b9;color:white;padding:12px 24px;text-decoration:none;border-radius:4px;display:inline-block">
              Verify Payroll Details
            </a>
          </p>
          <p style="color:#888;font-size:12px">HR Department | Your Company</p>
        </div>
        """,
    },
    "ceo_urgent_request": {
        "subject": "Urgent request from the CEO - Confidential",
        "sender_name": "CEO Office",
        "body_html": """
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #ddd;padding:24px">
          <h2>Urgent & Confidential</h2>
          <p>Hi {name},</p>
          <p>I need you to review and sign an important document before the board meeting today. Please access it through the secure portal below.</p>
          <p>This is time-sensitive. Please do not discuss with others until after the meeting.</p>
          <p style="text-align:center">
            <a href="{link}" style="background:#27ae60;color:white;padding:12px 24px;text-decoration:none;border-radius:4px;display:inline-block">
              View Confidential Document
            </a>
          </p>
          <p>Thanks,<br>Office of the CEO</p>
        </div>
        """,
    },
    "shared_file_notification": {
        "subject": "Someone shared a file with you on Company Drive",
        "sender_name": "Company Drive",
        "body_html": """
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #ddd;padding:24px">
          <h2 style="color:#4285f4">📄 A file has been shared with you</h2>
          <p>Hi {name},</p>
          <p><strong>Finance Team</strong> has shared a document with you:</p>
          <div style="background:#f8f8f8;padding:16px;border-radius:4px;margin:16px 0">
            <strong>Q4 Salary Review - Confidential.xlsx</strong>
          </div>
          <p style="text-align:center">
            <a href="{link}" style="background:#4285f4;color:white;padding:12px 24px;text-decoration:none;border-radius:4px;display:inline-block">
              Open Document
            </a>
          </p>
          <p style="color:#888;font-size:12px">Company Drive Notification System</p>
        </div>
        """,
    },
}

# ─────────────────────────────────────────────
# LANDING PAGE (simulated credential harvester)
# ─────────────────────────────────────────────

LANDING_PAGE_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Secure Login</title>
  <style>
    body { font-family: Arial, sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; margin:0; background:#f0f2f5; }
    .box { background:white; padding:40px; border-radius:8px; box-shadow:0 2px 12px rgba(0,0,0,.15); width:360px; }
    h2 { margin-top:0; color:#333; }
    input { width:100%; padding:10px; margin:8px 0 16px; border:1px solid #ccc; border-radius:4px; box-sizing:border-box; font-size:14px; }
    button { width:100%; padding:12px; background:#0066cc; color:white; border:none; border-radius:4px; cursor:pointer; font-size:16px; }
    button:hover { background:#0055aa; }
    .note { font-size:12px; color:#888; margin-top:16px; text-align:center; }
  </style>
</head>
<body>
  <div class="box">
    <h2>Company Portal Login</h2>
    <p style="color:#555;font-size:14px">Your session has expired. Please sign in again.</p>
    <form method="POST" action="/capture/{{ token }}">
      <label style="font-size:13px">Email</label>
      <input type="email" name="email" placeholder="you@company.com" required>
      <label style="font-size:13px">Password</label>
      <input type="password" name="password" placeholder="Password" required>
      <button type="submit">Sign In</button>
    </form>
    <p class="note">Secured by Company IT Security</p>
  </div>
</body>
</html>
"""

AWARENESS_PAGE_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Security Awareness Training</title>
  <style>
    body { font-family: Arial, sans-serif; display:flex; justify-content:center; align-items:center; min-height:100vh; margin:0; background:#fff3cd; }
    .box { background:white; padding:40px; border-radius:8px; box-shadow:0 2px 12px rgba(0,0,0,.15); max-width:560px; text-align:center; }
    h1 { color:#e67e22; }
    .badge { font-size:64px; }
    p { color:#555; line-height:1.6; }
    .tips { background:#f8f9fa; border-radius:6px; padding:16px; text-align:left; margin-top:20px; }
    .tips li { margin:8px 0; font-size:14px; }
  </style>
</head>
<body>
  <div class="box">
    <div class="badge">⚠️</div>
    <h1>This Was a Phishing Test</h1>
    <p>You clicked a simulated phishing link sent as part of your company's <strong>Security Awareness Program</strong>. No real harm was done — your credentials were <strong>not captured</strong>.</p>
    <div class="tips">
      <strong>How to spot phishing emails:</strong>
      <ul>
        <li>Check the sender's actual email address carefully</li>
        <li>Hover over links before clicking — verify the URL</li>
        <li>Be suspicious of urgency ("Act now!", "24 hours")</li>
        <li>Never enter credentials from an email link — go directly to the site</li>
        <li>When in doubt, call IT or your manager directly</li>
      </ul>
    </div>
    <p style="margin-top:24px;font-size:13px;color:#888">This test was conducted by your IT Security team. Results are reported anonymously for training purposes.</p>
  </div>
</body>
</html>
"""

# ─────────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────────

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Phishing Sim - Admin Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin:0; background:#f4f6f8; }
    .nav { background:#2c3e50; color:white; padding:16px 32px; display:flex; align-items:center; gap:24px; }
    .nav h1 { margin:0; font-size:20px; }
    .nav a { color:#bdc3c7; text-decoration:none; font-size:14px; }
    .nav a:hover { color:white; }
    .container { max-width:1100px; margin:32px auto; padding:0 16px; }
    .cards { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:32px; }
    .card { background:white; border-radius:8px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,.1); }
    .card .num { font-size:36px; font-weight:bold; color:#2c3e50; }
    .card .label { font-size:13px; color:#888; margin-top:4px; }
    .card.red .num { color:#e74c3c; }
    .card.orange .num { color:#e67e22; }
    .card.green .num { color:#27ae60; }
    table { width:100%; border-collapse:collapse; background:white; border-radius:8px; overflow:hidden; box-shadow:0 1px 4px rgba(0,0,0,.1); }
    th { background:#2c3e50; color:white; padding:12px 16px; text-align:left; font-size:13px; }
    td { padding:12px 16px; font-size:13px; border-bottom:1px solid #f0f0f0; }
    tr:last-child td { border-bottom:none; }
    .badge { display:inline-block; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:bold; }
    .badge.clicked { background:#fdecea; color:#e74c3c; }
    .badge.submitted { background:#fdf0e0; color:#e67e22; }
    .badge.sent { background:#eaf4fb; color:#2980b9; }
    .badge.reported { background:#eafaf1; color:#27ae60; }
    h2 { color:#2c3e50; margin-bottom:16px; }
    .section { margin-bottom:32px; }
    form { background:white; border-radius:8px; padding:24px; box-shadow:0 1px 4px rgba(0,0,0,.1); }
    input, select, textarea { width:100%; padding:8px 10px; border:1px solid #ddd; border-radius:4px; box-sizing:border-box; margin-top:4px; font-size:13px; }
    label { font-size:13px; color:#555; display:block; margin-top:12px; }
    button { margin-top:16px; padding:10px 24px; background:#2c3e50; color:white; border:none; border-radius:4px; cursor:pointer; font-size:14px; }
    button:hover { background:#1a252f; }
    .alert { padding:12px 16px; border-radius:4px; margin-bottom:16px; font-size:13px; }
    .alert.success { background:#eafaf1; color:#27ae60; border:1px solid #a9dfbf; }
  </style>
</head>
<body>
<div class="nav">
  <h1>🎣 Phishing Sim</h1>
  <a href="/">Dashboard</a>
  <a href="/admin/campaign/new">New Campaign</a>
  <a href="/admin/report">Reports</a>
  <span style="margin-left:auto;font-size:12px;color:#7f8c8d">Internal Use Only — Security Team</span>
</div>
<div class="container">

  {% if message %}
  <div class="alert success">{{ message }}</div>
  {% endif %}

  <div class="cards">
    <div class="card"><div class="num">{{ stats.total_targets }}</div><div class="label">Total Targets</div></div>
    <div class="card red"><div class="num">{{ stats.clicked }}</div><div class="label">Clicked Link ({{ stats.click_rate }}%)</div></div>
    <div class="card orange"><div class="num">{{ stats.submitted }}</div><div class="label">Submitted Credentials ({{ stats.submit_rate }}%)</div></div>
    <div class="card green"><div class="num">{{ stats.reported }}</div><div class="label">Reported Suspicious</div></div>
  </div>

  <div class="section">
    <h2>Campaigns</h2>
    <table>
      <tr><th>Campaign</th><th>Template</th><th>Targets</th><th>Clicked</th><th>Submitted</th><th>Created</th></tr>
      {% for c in campaigns %}
      <tr>
        <td>{{ c.name }}</td>
        <td>{{ c.template }}</td>
        <td>{{ c.target_count }}</td>
        <td><span class="badge clicked">{{ c.clicked }}</span></td>
        <td><span class="badge submitted">{{ c.submitted }}</span></td>
        <td>{{ c.created_at }}</td>
      </tr>
      {% endfor %}
    </table>
  </div>

  <div class="section">
    <h2>Recent Activity</h2>
    <table>
      <tr><th>Name</th><th>Email</th><th>Department</th><th>Campaign</th><th>Status</th><th>IP</th><th>Time</th></tr>
      {% for t in recent %}
      <tr>
        <td>{{ t.name or '—' }}</td>
        <td>{{ t.email }}</td>
        <td>{{ t.department or '—' }}</td>
        <td>{{ t.campaign.name }}</td>
        <td>
          {% if t.submitted_at %}<span class="badge submitted">Submitted Creds</span>
          {% elif t.clicked_at %}<span class="badge clicked">Clicked</span>
          {% elif t.reported %}<span class="badge reported">Reported</span>
          {% else %}<span class="badge sent">Sent Only</span>{% endif %}
        </td>
        <td>{{ t.ip_address or '—' }}</td>
        <td>{{ (t.clicked_at or t.sent_at or '—') }}</td>
      </tr>
      {% endfor %}
    </table>
  </div>
</div>
</body>
</html>
"""

NEW_CAMPAIGN_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>New Campaign</title>
  <style>
    body { font-family: Arial, sans-serif; margin:0; background:#f4f6f8; }
    .nav { background:#2c3e50; color:white; padding:16px 32px; }
    .nav h1 { margin:0; font-size:20px; }
    .container { max-width:700px; margin:32px auto; padding:0 16px; }
    form { background:white; border-radius:8px; padding:32px; box-shadow:0 1px 4px rgba(0,0,0,.1); }
    label { font-size:13px; color:#555; display:block; margin-top:16px; font-weight:bold; }
    input, select, textarea { width:100%; padding:10px; border:1px solid #ddd; border-radius:4px; box-sizing:border-box; margin-top:6px; font-size:14px; }
    textarea { height:160px; font-family:monospace; }
    button { margin-top:24px; padding:12px 32px; background:#2c3e50; color:white; border:none; border-radius:4px; cursor:pointer; font-size:15px; }
    button:hover { background:#1a252f; }
    .hint { font-size:11px; color:#888; margin-top:4px; }
    h2 { margin-top:0; color:#2c3e50; }
  </style>
</head>
<body>
<div class="nav"><h1>🎣 Phishing Sim — New Campaign</h1></div>
<div class="container">
<form method="POST" action="/admin/campaign/create">
  <h2>Create New Phishing Campaign</h2>

  <label>Campaign Name</label>
  <input type="text" name="name" placeholder="e.g. Q1 2025 IT Password Test" required>

  <label>Email Template</label>
  <select name="template">
    {% for key, tpl in templates.items() %}
    <option value="{{ key }}">{{ key }} — {{ tpl.subject[:60] }}</option>
    {% endfor %}
  </select>

  <label>Target Employees (CSV format)</label>
  <div class="hint">Format: email, name, department (one per line). Name and department are optional.</div>
  <textarea name="targets" placeholder="john.doe@company.com, John Doe, Engineering&#10;jane.smith@company.com, Jane Smith, Finance&#10;bob@company.com"></textarea>

  <label>Sender Email (From address)</label>
  <input type="email" name="sender_email" placeholder="itsupport@company-helpdesk.com" required>
  <div class="hint">Use a domain you control for testing. Do NOT use your real company domain without authorization.</div>

  <label>SMTP Server</label>
  <input type="text" name="smtp_host" placeholder="smtp.gmail.com" value="smtp.gmail.com">

  <label>SMTP Port</label>
  <input type="number" name="smtp_port" value="587">

  <label>SMTP Username</label>
  <input type="text" name="smtp_user" placeholder="your-email@gmail.com">
  <div class="hint">⚠️ For Gmail: Use your FULL email address (e.g., yourname@gmail.com)</div>

  <label>SMTP Password (Gmail App Password)</label>
  <input type="password" name="smtp_pass" placeholder="16-character app password (used only for local/SMTP mode)">
  <div class="hint" style="color:#e74c3c">⚠️ <strong>For Gmail SMTP (local only):</strong> Use a 16-character App Password from <a href="https://myaccount.google.com/apppasswords" target="_blank">myaccount.google.com/apppasswords</a>.<br>
  <strong>On Render (production):</strong> Set the <code>SENDGRID_API_KEY</code> environment variable — SMTP fields are ignored and SendGrid is used instead.</div>

  <label>Tracking Base URL</label>
  <input type="text" name="base_url" placeholder="http://your-server-ip:5000" required>
  <div class="hint">The URL where this server is reachable by employees. Use a neutral domain to avoid suspicion.</div>

  <button type="submit">Launch Campaign</button>
</form>
</div>
</body>
</html>
"""

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def dashboard():
    campaigns_raw = Campaign.query.order_by(Campaign.created_at.desc()).all()
    campaigns = []
    for c in campaigns_raw:
        campaigns.append({
            "name": c.name,
            "template": c.template,
            "target_count": len(c.targets),
            "clicked": sum(1 for t in c.targets if t.clicked_at),
            "submitted": sum(1 for t in c.targets if t.submitted_at),
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M"),
        })

    all_targets = Target.query.all()
    total = len(all_targets)
    clicked = sum(1 for t in all_targets if t.clicked_at)
    submitted = sum(1 for t in all_targets if t.submitted_at)
    reported = sum(1 for t in all_targets if t.reported)

    stats = {
        "total_targets": total,
        "clicked": clicked,
        "submitted": submitted,
        "reported": reported,
        "click_rate": round(clicked / total * 100, 1) if total else 0,
        "submit_rate": round(submitted / total * 100, 1) if total else 0,
    }

    recent = Target.query.options(joinedload(Target.campaign)).order_by(Target.clicked_at.desc().nullslast()).limit(50).all()
    return render_template_string(DASHBOARD_HTML, stats=stats, campaigns=campaigns, recent=recent, message=request.args.get("msg"))

@app.route("/admin/campaign/new")
def new_campaign():
    return render_template_string(NEW_CAMPAIGN_HTML, templates=EMAIL_TEMPLATES)

@app.route("/admin/campaign/create", methods=["POST"])
def create_campaign():
    data = request.form
    campaign = Campaign(name=data["name"], template=data["template"])
    db.session.add(campaign)
    db.session.flush()

    targets_raw = data["targets"].strip().splitlines()
    targets = []
    for line in targets_raw:
        parts = [p.strip() for p in line.split(",")]
        if not parts[0]:
            continue
        t = Target(
            campaign_id=campaign.id,
            email=parts[0],
            name=parts[1] if len(parts) > 1 else "",
            department=parts[2] if len(parts) > 2 else "",
        )
        targets.append(t)
        db.session.add(t)

    db.session.commit()

    # Collect data needed by background thread (can't use request context in thread)
    smtp_host = data["smtp_host"]
    smtp_port = int(data["smtp_port"])
    smtp_user = data["smtp_user"]
    smtp_pass = data["smtp_pass"]
    sender_email = data["sender_email"]
    base_url = data["base_url"].rstrip("/")
    template = EMAIL_TEMPLATES[data["template"]]
    target_ids = [t.id for t in targets]

    def send_emails_background():
        with app.app_context():
            try:
                sg_key = os.getenv("SENDGRID_API_KEY", "")
                if sg_key:
                    # ── SendGrid HTTP API (works on Render free tier) ──
                    import sendgrid as sg_module
                    from sendgrid.helpers.mail import Mail
                    sg_client = sg_module.SendGridAPIClient(sg_key)
                    print(f"[EMAIL] Using SendGrid, sending to {len(target_ids)} targets")
                    for tid in target_ids:
                        t = db.session.get(Target, tid)
                        if t is None:
                            continue
                        link = f"{base_url}/click/{t.token}"
                        body = template["body_html"].replace("{name}", t.name or "Team Member").replace("{link}", link)
                        mail = Mail(
                            from_email=f'{template["sender_name"]} <{sender_email}>',
                            to_emails=t.email,
                            subject=template["subject"],
                            html_content=body,
                        )
                        response = sg_client.send(mail)
                        print(f"[EMAIL] SendGrid → {t.email}: HTTP {response.status_code}")
                        t.sent_at = datetime.utcnow()
                    db.session.commit()
                    print("[EMAIL] All emails dispatched via SendGrid")
                else:
                    # ── SMTP fallback (localhost / non-Render) ──
                    print(f"[SMTP] Connecting to {smtp_host}:{smtp_port} as {smtp_user}")
                    if smtp_port == 465:
                        ctx = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30)
                    else:
                        ctx = smtplib.SMTP(smtp_host, smtp_port, timeout=30)
                        ctx.starttls()
                    ctx.login(smtp_user, smtp_pass)
                    print(f"[SMTP] Login OK, sending to {len(target_ids)} targets")
                    for tid in target_ids:
                        t = db.session.get(Target, tid)
                        if t is None:
                            continue
                        link = f"{base_url}/click/{t.token}"
                        body = template["body_html"].replace("{name}", t.name or "Team Member").replace("{link}", link)
                        msg = MIMEMultipart("alternative")
                        msg["Subject"] = template["subject"]
                        msg["From"] = f'{template["sender_name"]} <{sender_email}>'
                        msg["To"] = t.email
                        msg.attach(MIMEText(body, "html"))
                        ctx.sendmail(sender_email, t.email, msg.as_string())
                        t.sent_at = datetime.utcnow()
                        print(f"[SMTP] Sent to {t.email}")
                    ctx.quit()
                    db.session.commit()
                    print("[SMTP] All emails sent")
            except Exception as e:
                import traceback
                print(f"[EMAIL ERROR] {type(e).__name__}: {e}")
                print(traceback.format_exc())

    threading.Thread(target=send_emails_background, daemon=True).start()
    return redirect(f"/?msg=Campaign+launched!+Sending+{len(target_ids)}+emails+in+background.")

@app.route("/click/<token>")
def track_click(token):
    target = Target.query.filter_by(token=token).first()
    if target and not target.clicked_at:
        target.clicked_at = datetime.utcnow()
        target.ip_address = request.remote_addr
        target.user_agent = request.user_agent.string
        db.session.commit()
    return render_template_string(LANDING_PAGE_HTML, token=token)

@app.route("/capture/<token>", methods=["POST"])
def capture_submit(token):
    target = Target.query.filter_by(token=token).first()
    if target and not target.submitted_at:
        target.submitted_at = datetime.utcnow()
        # NOTE: Credentials are intentionally NOT stored — only the event is recorded.
        db.session.commit()
    return render_template_string(AWARENESS_PAGE_HTML)

@app.route("/report/<token>")
def report_phish(token):
    """Employee can use this link to report the phishing email."""
    target = Target.query.filter_by(token=token).first()
    if target:
        target.reported = True
        db.session.commit()
    return "<h2>Thank you for reporting! Your security team has been notified.</h2>"

@app.route("/admin/test-smtp")
def test_smtp():
    """Quick SMTP connectivity test — returns result directly in browser."""
    import traceback
    host  = request.args.get("host", "smtp.gmail.com")
    port  = int(request.args.get("port", 587))
    user  = request.args.get("user", "")
    pw    = request.args.get("pw", "")
    if not user or not pw:
        return ("<pre>Usage: /admin/test-smtp?host=smtp.gmail.com&port=587"
                "&user=you@gmail.com&pw=apppassword</pre>")
    try:
        if port == 465:
            s = smtplib.SMTP_SSL(host, port, timeout=15)
        else:
            s = smtplib.SMTP(host, port, timeout=15)
            s.starttls()
        s.login(user, pw)
        s.quit()
        return f"<pre style='color:green'>SUCCESS: logged in as {user} via {host}:{port}</pre>"
    except Exception as e:
        return f"<pre style='color:red'>FAILED ({type(e).__name__}): {e}\n\n{traceback.format_exc()}</pre>"


@app.route("/admin/report")
def export_report():
    """Export CSV report for audit."""
    import io
    targets = Target.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Campaign", "Email", "Name", "Department", "Sent At", "Clicked At", "Submitted At", "Reported", "IP Address", "User Agent"])
    for t in targets:
        writer.writerow([
            t.campaign.name,
            t.email,
            t.name or "",
            t.department or "",
            t.sent_at or "",
            t.clicked_at or "",
            t.submitted_at or "",
            "Yes" if t.reported else "No",
            t.ip_address or "",
            t.user_agent or "",
        ])
    output.seek(0)
    from flask import Response
    return Response(output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=phishing_report.csv"})

# ─────────────────────────────────────────────
# INIT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # also initialise synchronously for direct runs
    
    # Support both local development and production deployment
    port = int(os.getenv("PORT", 5000))
    
    print("\n Phishing Simulation System running")
    print(f" Server: http://0.0.0.0:{port}")
    print(" FOR INTERNAL SECURITY TESTING USE ONLY\n")
    app.run(host="0.0.0.0", port=port, debug=False)
