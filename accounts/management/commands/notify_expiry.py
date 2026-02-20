"""
Management command to send subscription expiry warning emails.
Sends warnings to users whose subscription expires within 3 days.

Usage:
    python manage.py notify_expiry

Schedule this to run daily via cron or Task Scheduler.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from accounts.models import UserProfile
from accounts.emails import send_subscription_expiry_warning


class Command(BaseCommand):
    help = 'Send subscription expiry warning emails (3 days before expiry)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=3,
            help='Number of days before expiry to send warning (default: 3)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview which users would receive emails without actually sending',
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        now = timezone.now()

        # Find users whose subscription expires within the specified window
        expiry_start = now
        expiry_end = now + timezone.timedelta(days=days)

        profiles = UserProfile.objects.filter(
            subscription_expiry__gt=expiry_start,
            subscription_expiry__lte=expiry_end,
        ).select_related('user')

        if not profiles.exists():
            self.stdout.write(self.style.SUCCESS('No subscriptions expiring within the next {} day(s).'.format(days)))
            return

        self.stdout.write(f'Found {profiles.count()} subscription(s) expiring within {days} day(s):')

        sent_count = 0
        failed_count = 0

        for profile in profiles:
            days_remaining = (profile.subscription_expiry - now).days
            if days_remaining < 1:
                days_remaining = 1  # Show "1 day" minimum

            if dry_run:
                self.stdout.write(f'  [DRY RUN] {profile.user.email} — expires {profile.subscription_expiry.strftime("%Y-%m-%d")} ({days_remaining}d remaining)')
            else:
                success = send_subscription_expiry_warning(profile, days_remaining)
                if success:
                    sent_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ {profile.user.email} — {days_remaining}d remaining'))
                else:
                    failed_count += 1
                    self.stdout.write(self.style.ERROR(f'  ✗ {profile.user.email} — email failed'))

        if not dry_run:
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS(f'Done. Sent: {sent_count}, Failed: {failed_count}'))
