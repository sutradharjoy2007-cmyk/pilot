import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userpanel_project.settings')
django.setup()

User = get_user_model()
user = User.objects.first()
if not user:
    print("No user found")
    exit(1)

print(f"Testing with user: {user.email}")

c = Client()
c.force_login(user)

# Test AJAX POST
response = c.post(
    '/ai-agent/',
    {
        'facebook_page_id': '123456', 
        'facebook_page_api': 'api_key_test',
        'is_active': 'on',
        'blocked_post_ids': '123\n456'
    },
    HTTP_X_REQUESTED_WITH='XMLHttpRequest'
)

print(f"Status Code: {response.status_code}")
print(f"Content Type: {response.headers.get('Content-Type')}")
print(f"Content: {response.content.decode()}")
