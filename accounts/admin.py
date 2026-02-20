from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.conf import settings
from .models import CustomUser, UserProfile, AIAgentConfig, SubscriptionHistory
from .emails import send_kyc_approved_email, send_kyc_rejected_email


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']



class SubscriptionHistoryInline(admin.TabularInline):
    model = SubscriptionHistory
    extra = 0
    readonly_fields = ['start_date', 'package_name', 'expiry_date', 'created_at']
    can_delete = False
    ordering = ('-created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'kyc_status', 'kyc_document_links', 'subscription_expiry', 'package_name']
    list_filter = ['kyc_status', 'package_name']
    actions = ['approve_kyc', 'reject_kyc', 'assign_7_days', 'assign_15_days', 'assign_30_days']
    readonly_fields = ['kyc_front_preview', 'kyc_back_preview']
    inlines = [SubscriptionHistoryInline]
    
    def kyc_document_links(self, obj):
        from django.utils.html import format_html
        from django.utils.safestring import mark_safe
        links = []
        if obj.kyc_front_image:
            links.append(format_html('<a href="{}" target="_blank">Front</a>', obj.kyc_front_image.url))
        if obj.kyc_back_image:
            links.append(format_html('<a href="{}" target="_blank">Back</a>', obj.kyc_back_image.url))
        return mark_safe(" | ".join(links)) if links else "No documents"
    kyc_document_links.short_description = "KYC Documents"
    
    def kyc_front_preview(self, obj):
        from django.utils.html import format_html
        if obj.kyc_front_image:
            return format_html('<img src="{}" style="max-width:300px; max-height:200px;" />', obj.kyc_front_image.url)
        return "No front image uploaded"
    kyc_front_preview.short_description = "Front ID Preview"

    def kyc_back_preview(self, obj):
        from django.utils.html import format_html
        if obj.kyc_back_image:
            return format_html('<img src="{}" style="max-width:300px; max-height:200px;" />', obj.kyc_back_image.url)
        return "No back image uploaded"
    kyc_back_preview.short_description = "Back ID Preview"
    
    @admin.action(description="✅ Approve KYC Verification")
    def approve_kyc(self, request, queryset):
        # Collect IDs first, then bulk-update, then re-fetch fresh profiles
        user_ids = list(queryset.values_list('id', flat=True))
        updated_count = queryset.update(kyc_status='VERIFIED', kyc_rejection_reason='')

        # Re-fetch profiles so we have fresh data after the bulk update
        for profile in UserProfile.objects.filter(id__in=user_ids).select_related('user'):
            send_kyc_approved_email(profile)

        self.message_user(request, f"{updated_count} user(s) KYC approved and notified by email.")
    approve_kyc.short_description = "✅ Approve KYC Verification"
    
    @admin.action(description="❌ Reject KYC Verification")
    def reject_kyc(self, request, queryset):
        # Collect IDs first, then bulk-update, then re-fetch fresh profiles
        user_ids = list(queryset.values_list('id', flat=True))
        updated_count = queryset.update(kyc_status='REJECTED')

        # Re-fetch profiles so we have fresh data (including any kyc_rejection_reason set elsewhere)
        for profile in UserProfile.objects.filter(id__in=user_ids).select_related('user'):
            # Set a default reason if none was provided
            if not profile.kyc_rejection_reason:
                profile.kyc_rejection_reason = 'Your KYC submission did not meet our requirements. Please re-submit with clear, high-resolution images of a valid NID or Passport.'
                profile.save(update_fields=['kyc_rejection_reason'])
            send_kyc_rejected_email(profile)

        self.message_user(request, f"{updated_count} user(s) KYC rejected and notified by email.")
    reject_kyc.short_description = "❌ Reject KYC Verification"
    
    def assign_days(self, request, queryset, days, package_name):
        from django.utils import timezone
        from datetime import timedelta
        
        expiry_date = timezone.now() + timedelta(days=days)
        
        updated_count = 0
        for profile in queryset:
            profile.subscription_expiry = expiry_date
            profile.package_name = package_name
            profile.save()
            
            # Create history record
            SubscriptionHistory.objects.create(
                profile=profile,
                package_name=package_name,
                expiry_date=expiry_date
            )
            updated_count += 1
            
        self.message_user(request, f"{updated_count} users assigned {package_name} package.")
    
    @admin.action(description="Assign 7 Days Package")
    def assign_7_days(self, request, queryset):
        self.assign_days(request, queryset, 7, "7 Days Pack")
    
    @admin.action(description="Assign 15 Days Package")
    def assign_15_days(self, request, queryset):
        self.assign_days(request, queryset, 15, "15 Days Pack")
    
    @admin.action(description="Assign 30 Days Package")
    def assign_30_days(self, request, queryset):
        self.assign_days(request, queryset, 30, "30 Days Pack")
 

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(UserProfile) # Replaced with custom admin class
admin.site.register(AIAgentConfig)

# Custom Admin Dashboard Template
admin.site.index_template = 'admin/custom_dashboard.html'
