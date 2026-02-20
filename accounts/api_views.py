from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import CustomUser, AIAgentConfig, UserProfile


@csrf_exempt
def api_get_user_config(request, admin_password, email_prefix, field):
    """
    Public API endpoint to access user AI configuration
    URL: /api/user/{admin_password}/{email_prefix}/{field}
    
    Fields available:
    - fb_page_id: Returns Facebook Page ID
    - fb_page_api: Returns Facebook Page API key
    - system_prompt: Returns AI system prompt
    - webhook_url: Returns webhook URL
    - ai_agent_status: Returns whether AI agent is on or off
    - block_post_ids: Returns list of blocked Facebook post IDs
    - all: Returns all configuration as JSON
    """
    
    # Verify admin password
    if admin_password != settings.API_ADMIN_PASSWORD:
        return HttpResponse('Unauthorized', status=401)
    
    try:
        # Find user by email prefix
        user = CustomUser.objects.filter(email__startswith=email_prefix + '@').first()
        
        if not user:
            # Try exact match if no @ symbol
            users = CustomUser.objects.filter(email__icontains=email_prefix)
            if users.exists():
                user = users.first()
            else:
                return HttpResponse('User not found', status=404)
        
        # Get AI config
        try:
            ai_config = user.ai_config
        except AIAgentConfig.DoesNotExist:
            return HttpResponse('AI configuration not found for this user', status=404)
        
        # Check subscription status — if expired, agent is effectively off
        try:
            profile = user.profile
            subscription_active = profile.is_subscription_active()
        except UserProfile.DoesNotExist:
            subscription_active = False
        
        effective_active = ai_config.is_active and subscription_active
        
        # Return requested field
        if field == 'fb_page_id':
            return HttpResponse(ai_config.facebook_page_id or '', content_type='text/plain')
        
        elif field == 'system_prompt':
            return HttpResponse(ai_config.system_prompt or '', content_type='text/plain')
        
        elif field == 'webhook_url':
            return HttpResponse(ai_config.get_webhook_url(), content_type='text/plain')
        
        elif field == 'fb_page_api':
            return HttpResponse(ai_config.facebook_page_api or '', content_type='text/plain')
        
        elif field == 'ai_agent_status':
            status = 'on' if effective_active else 'off'
            return JsonResponse({'status': status})
        
        elif field == 'block_post_ids':
            # User said: "i will get all the list of block FB post ids"
            blocked_ids = ai_config.get_blocked_post_ids_list()
            return JsonResponse({'blocked_post_ids': blocked_ids})
        
        elif field == 'all':
            blocked_ids = ai_config.get_blocked_post_ids_list()
            data = {
                'email': user.email,
                'email_prefix': user.get_email_prefix(),
                'ai_agent_status': 'on' if effective_active else 'off',
                'is_active': effective_active,
                'subscription_active': subscription_active,
                'fb_page_id': ai_config.facebook_page_id or '',
                'fb_page_api': ai_config.facebook_page_api or '',
                'system_prompt': ai_config.system_prompt or '',
                'webhook_url': ai_config.get_webhook_url(),
                'blocked_post_ids': blocked_ids,
            }
            return JsonResponse(data)
        
        else:
            return HttpResponse(
                'Invalid field. Available fields: fb_page_id, fb_page_api, system_prompt, webhook_url, ai_agent_status, block_post_ids, all',
                status=400
            )
    
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
