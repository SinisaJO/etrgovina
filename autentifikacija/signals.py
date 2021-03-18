from prodavnica.models import Kupac
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def customer_profile(sender, instance, created, **kwargs):
	if created:
		Kupac.objects.create(
            kupac=instance,
			name=instance.username,
			)
		print('Profile created!')

post_save.connect(customer_profile, sender=User)