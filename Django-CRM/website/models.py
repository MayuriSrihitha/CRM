from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Record(models.Model):
	STATUS_CHOICES = [
		('initiated', 'Initiated'),
		('in_progress', 'In Progress'),
		('closed', 'Closed'),
	]
	
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.CharField(max_length=100)
	phone = models.CharField(max_length=15)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	zipcode = models.CharField(max_length=20)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='initiated')
	assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_records')
	last_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return(f"{self.first_name} {self.last_name}")


class UserProfile(models.Model):
	USER_TYPES = [
		('admin', 'Admin'),
		('regular', 'Regular User'),
	]
	
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_type = models.CharField(max_length=10, choices=USER_TYPES, default='regular')
	
	def __str__(self):
		return f"{self.user.username} - {self.user_type}"

# Modified signal handlers
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)
	else:
		try:
			instance.userprofile.save()
		except UserProfile.DoesNotExist:
			UserProfile.objects.create(user=instance)
