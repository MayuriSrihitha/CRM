from django.db import migrations

def create_user_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('website', 'UserProfile')
    
    for user in User.objects.all():
        UserProfile.objects.get_or_create(
            user=user,
            defaults={'user_type': 'admin' if user.is_superuser else 'regular'}
        )

class Migration(migrations.Migration):
    dependencies = [
        ('website', '0001_initial'),  # Adjust this to your last migration
    ]

    operations = [
        migrations.RunPython(create_user_profiles),
    ]
