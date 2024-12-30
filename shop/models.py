from django.db import models
from django.utils.translation import gettext_lazy as _ 
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('body'), blank=True)
    top_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    
    def __str__(self):
        return self.title
    

class Discount(models.Model):
    discount = models.FloatField(verbose_name=_('discount'))
    description = models.TextField(verbose_name=_('description'))
    

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='product_image', null=True, blank=True)
    inventory = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    discount = models.ManyToManyField('Discount', blank=True, related_name='products')
    datetime_created = models.DateTimeField(default=timezone.now , verbose_name=_('date of created'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('date of modified'))
    
    def __str__(self):
        return self.name
    

class Customer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('first_name'))    
    last_name = models.CharField(max_length=100, verbose_name=_('last_name'))
    phone_number = models.CharField(max_length=250, verbose_name=_('phone_number'))
    birth_date = models.DateField(verbose_name=_('birthdate'), null=True, blank=True)
    email = models.EmailField(verbose_name=_('email'), blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
class Address(models.Model):
    customer = models.OneToOneField("Customer", on_delete=models.CASCADE, primary_key=True)
    province = models.CharField(max_length=100, verbose_name=_('province'))
    city = models.CharField(max_length=100, verbose_name=_('city'))
    address_detail = models.TextField(verbose_name=_('street'))


class UnpaidOrderMethod(models.Manager):
    def get_unpaid(self):
        return self.get_queryset().filter(status=Order.ORDER_STATUS_UNPAID)


class UnpaidOrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.ORDER_STATUS_UNPAID)
    

class StatusOrderMethod(models.Manager):
    def get_by_status(self, status):
        if status in [Order.ORDER_STATUS_PAID, Order.ORDER_STATUS_UNPAID, Order.ORDER_STATUS_CANCELED]:
            return self.get_queryset().filter(status=status)
        return self.get_queryset()


class Order(models.Model):
    ORDER_STATUS_PAID = 'P'
    ORDER_STATUS_UNPAID = 'UN'
    ORDER_STATUS_CANCELED = 'C'
    ORDER_STATUS = (
        (ORDER_STATUS_UNPAID, 'Unpaid'),
        (ORDER_STATUS_PAID, 'Paid'),
        (ORDER_STATUS_CANCELED, 'Canceled')
    )
    
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, related_name='orders')
    datetime_created = models.DateTimeField(default=timezone.now , verbose_name=_('date of created'))
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default=ORDER_STATUS_UNPAID)
    
    # manager
    objects = StatusOrderMethod()
    unpaided = UnpaidOrderManager()
    
    def __str__(self):
        return f"{self.customer} --> order_id :{self.id}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name=_('quantity'))
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = [['order', 'product']]
        
        
class Cart(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('created_at'))


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.PROTECT, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name=_('quantity'))
    
    class Meta:
        unique_together = [['cart', 'product']]


class ApprovedCommentMethod(models.Manager):
    def get_approved(self):
        return self.get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED)
    
    
class ApprovedCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Comment.COMMENT_STATUS_APPROVED)
    

class Comment(models.Model):
    COMMENT_STATUS_NOT_APPROVED = 'NA'
    COMMENT_STATUS_APPROVED = 'A'
    COMMENT_STATUS_WAITING = 'W'
    COMMENT_STATUS = (
        (COMMENT_STATUS_NOT_APPROVED, _('Not Approved')),
        (COMMENT_STATUS_APPROVED, _('Approved')),
        (COMMENT_STATUS_WAITING, _('Waiting'))
    )
    body = models.TextField(verbose_name=_('text'))
    name = models.CharField(max_length=100)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
    status = models.CharField(max_length=20, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)
    datetime_created = models.DateTimeField(default=timezone.now , verbose_name=_('date of created'))

    # managers
    objects = models.Manager()
    approved = ApprovedCommentManager()
    # approved_comment = ApprovedComment()
    