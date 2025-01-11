from django.dispatch import receiver
from shop.signals import order_created


@receiver(order_created)
def after_order_created(sender, **kwargs):
     print(f"New order created from {kwargs['order'].id}")
     
