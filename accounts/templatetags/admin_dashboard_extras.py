from django import template
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser

register = template.Library()

@register.simple_tag
def get_new_users():
    """Returns users who joined today"""
    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return CustomUser.objects.filter(date_joined__gte=start_of_day).order_by('-date_joined')
