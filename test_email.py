import os
import django
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userpanel_project.settings')
django.setup()

try:
    print("Attempting to send email...")
    send_mail(
        'Test Subject',
        'Test Message',
        settings.DEFAULT_FROM_EMAIL,
        ['sutradharjoy2006@gmail.com'],
        fail_silently=False,
    )
    print("Email sent successfully!")
except Exception as e:
    print(f"Error sending email: {e}")
