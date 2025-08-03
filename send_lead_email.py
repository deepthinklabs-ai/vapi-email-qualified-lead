import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email
from dotenv import load_dotenv

load_dotenv()


def send_lead_email(name, phone, email, product_type, volume, summary):
    """
    Compose and send an email through SendGrid with the qualified-lead details.
    Raises any SendGrid error so the Flask route can return 500.
    """
    from_email = os.getenv("FROM_EMAIL", "from@example.com")
    to_email = os.getenv("TO_EMAIL", "to@example.com")
    reply_to_email = os.getenv("REPLY_TO_EMAIL", from_email)

    message = Mail(
        from_email=Email(from_email, name="Lead Notification Bot"),
        to_emails=to_email,
        subject=f"🚨 New Qualified Lead: {name}",
        plain_text_content=(
            f"A new qualified lead was captured.\n\n"
            f"Name: {name}\n"
            f"Phone: {phone}\n"
            f"Email: {email}\n"
            f"Product Type: {product_type}\n"
            f"Volume: {volume}\n\n"
            f"📞 Call Summary:\n{summary}\n"
        ),
    )
    message.reply_to = Email(reply_to_email)

    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    response = sg.send(message)
    print(f"Email sent – SendGrid status {response.status_code}")  # 202 = accepted
