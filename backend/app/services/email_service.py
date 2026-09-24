"""
Email service for sending reset codes and notifications.

For development, codes are printed to console.
For production, configure SMTP settings in .env and uncomment send_email.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send email via SMTP.
    Returns True if sent, False if email not configured.
    """
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")

    if not all([smtp_server, smtp_user, smtp_pass]):
        # Email not configured — just log
        print(f"\n📧 EMAIL (not sent — SMTP not configured)")
        print(f"   To:      {to_email}")
        print(f"   Subject: {subject}")
        print(f"   Body:    {body}\n")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


def send_reset_code(to_email: str, code: str) -> bool:
    """Send password reset code via email."""
    subject = "NOMS — Password Reset Code"
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #2563eb;">NOMS Password Reset</h2>
        <p>Your password reset code is:</p>
        <div style="background: #f3f4f6; padding: 20px; text-align: center;
                    font-size: 32px; font-weight: bold; letter-spacing: 8px;
                    border-radius: 8px; color: #1e40af;">
          {code}
        </div>
        <p style="color: #6b7280; font-size: 14px; margin-top: 20px;">
          This code will expire in 15 minutes.<br>
          If you didn't request this, ignore this email.
        </p>
      </body>
    </html>
    """
    return send_email(to_email, subject, body)