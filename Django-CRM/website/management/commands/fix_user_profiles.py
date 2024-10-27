from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from website.models import UserProfile

class Command(BaseCommand):
    help = 'Creates missing UserProfiles and fixes existing ones'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        created_count = 0
        updated_count = 0
        
        for user in users:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                created_count += 1
                if user.is_superuser:
                    profile.user_type = 'admin'
                    profile.save()
                    updated_count += 1
                    
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} profiles and updated {updated_count} profiles'
            )
        )
