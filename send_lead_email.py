import os
import traceback                          # <─ NEW
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from dotenv import load_dotenv

load_dotenv()

def send_lead_email(name, phone, email, product_type, volume, summary):
    print("🔔 send_lead_email called")     # <─ NEW  (debug)

    from_email      = os.getenv("FROM_EMAIL", "from@example.com")
    to_email        = os.getenv("TO_EMAIL", "to@example.com")
    reply_to_email  = os.getenv("REPLY_TO_EMAIL", from_email)

    message = Mail(
        from_email=Email(from_email, name='Lead Notification Bot'),
        to_emails=to_email,
        subject=f'🚨 New Qualified Lead: {name}',
        plain_text_content=f"""
        A new qualified lead was captured.

        Name: {name}
        Phone: {phone}
        Email: {email}
        Product Type: {product_type}
        Volume: {volume}

        📞 Call Summary:
        {summary}
        """,
    )

    message.reply_to = Email(reply_to_email)

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(f"✅ Email sent! Status: {response.status_code}")
    except Exception as e:
        traceback.print_exc()              # <─ NEW  (debug)
        print(f"❌ SendGrid error: {e}")
