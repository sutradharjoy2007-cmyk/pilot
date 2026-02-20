from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)
            
        # Paths that are always allowed even if expired
        allowed_paths = [
            reverse('subscription_expired'),
            reverse('logout'),
            '/admin/',
        ]
        
        # Check if current path matches any allowed path
        for path in allowed_paths:
            if request.path.startswith(path):
                return self.get_response(request)
        
        # Check subscription status
        if hasattr(request.user, 'profile') and not request.user.profile.is_subscription_active():
            return redirect('subscription_expired')
            
        return self.get_response(request)
