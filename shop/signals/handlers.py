from django.db.models.signals import post_save,post_delete,post_migrate,post_init
from django.dispatch import receiver
from django.conf import settings

from shop.models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
