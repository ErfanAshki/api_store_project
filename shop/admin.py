from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from django.contrib import messages

from .models import Product, Cart, CartItem, Category, Comment, Customer ,Order, OrderItem, Discount, Address


class InventoryFilter(admin.SimpleListFilter):
    title = 'Critical Inventory Status'
    parameter_name = 'inventory'
    LESS_THAN_3 = '<3'
    BETWEEN_3_AND_10 = '3<=10'
    GREATER_THAN_10 = '>10'

    def lookups(self, request, model_admin):
        return [
            (InventoryFilter.LESS_THAN_3, 'High'),
            (InventoryFilter.BETWEEN_3_AND_10, 'Medium'),
            (InventoryFilter.GREATER_THAN_10, 'Ok')
        ]

    def queryset(self, request, queryset):
        if self.value() == InventoryFilter.LESS_THAN_3:
            return queryset.filter(inventory__lt=3)
        elif self.value() == InventoryFilter.BETWEEN_3_AND_10:
            return queryset.filter(inventory__range=(3, 10))
        elif self.value() == InventoryFilter.GREATER_THAN_10:
            return queryset.filter(inventory__gt=10)
        
        
class CommentInline(admin.StackedInline):
    model = Comment
    fields = ['id', 'product', 'name' , 'status', 'datetime_created']
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category_title' , 'unit_price', 'inventory', 'inventory_status', 'num_of_comments']
    ordering = ['id']
    list_per_page = 20    
    list_editable = ['unit_price', 'inventory']
    list_select_related = ['category']
    list_filter = [InventoryFilter, 'category']
    search_fields = ['name__istartswith']
    list_display_links = ['id', 'name']
    actions = ['clear_inventory']
    prepopulated_fields = {
        'slug': ['name', 'unit_price']
    }
    inlines = [CommentInline]
    
    def inventory_status(self, product):
        if product.inventory < 10 :
            return 'LOW'
        elif product.inventory > 50 : 
            return 'HIGH'
        else:
            return 'MEDIUM'
        
    @admin.display(ordering='category__title')
    def category_title(self , product):
        return product.category.title
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('comments'). \
            annotate(num_of_comments=Count('comments'))
    
    @admin.display(ordering='num_of_comments')
    def num_of_comments(self, product):
        url = (
            reverse('admin:shop_comment_changelist')
            + '?'
            + urlencode({
                'product__id': product.id
            })
        )
        
        return format_html(f"<a href='{url}'>{product.num_of_comments} </a>")
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(request, f"{update_count} inventories of products cleared.", messages.WARNING)

    
admin.site.register(Product, ProductAdmin)


class ItemsFilter(admin.SimpleListFilter):
    title = 'Items Of Orders'
    parameter_name = 'items'
    LESS_THAN_3 = '<3'
    BETWEEN_3_AND_7 = '3<=7'
    GREATER_THAN_7 = '>7'

    def lookups(self, request, model_admin):
        return [
            (ItemsFilter.LESS_THAN_3, 'Ok'),
            (ItemsFilter.BETWEEN_3_AND_7, 'Normal'),
            (ItemsFilter.GREATER_THAN_7, 'Lot')
        ]

    def queryset(self, request, queryset):
        if self.value() == ItemsFilter.LESS_THAN_3:
            return queryset.filter(items_count__lt=3)
        elif self.value() == ItemsFilter.BETWEEN_3_AND_7:
            return queryset.filter(items_count__lte=7, items_count__gte=3)
        elif self.value() == ItemsFilter.GREATER_THAN_7:
            return queryset.filter(items_count__gt=7)
    
    def get_queryset(self):
        queryset = super(self).get_queryset().annotate(items_count=Count('items'))
        return queryset
    

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    fields = ['id', 'order', 'product' , 'quantity', 'unit_price']
    extra = 1
    min_num = 1
    max_num = 20


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'datetime_created', 'number_of_items']
    ordering = ['id']
    list_per_page = 15    
    list_editable = ['status']
    list_filter = ['status', ItemsFilter]
    search_fields = ['customer__first_name', 'customer__last_name']
    list_display_links = ['id']
    inlines = [OrderItemInline]
    
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items'). \
            annotate(items_count=Count('items'))
    
    @admin.display(ordering='items_count')
    def number_of_items(self, order):
        return order.items_count
    
    
admin.site.register(Order, OrderAdmin)


class QuantityFilter(admin.SimpleListFilter):
    title = 'Quantity Status'
    parameter_name = 'quantity'
    LESS_THAN_3 = '<3'
    BETWEEN_3_AND_10 = '3<=10'
    GREATER_THAN_10 = '>10'

    def lookups(self, request, model_admin):
        return [
            (QuantityFilter.LESS_THAN_3, 'Ok'),
            (QuantityFilter.BETWEEN_3_AND_10, 'Good'),
            (QuantityFilter.GREATER_THAN_10, 'Very Good')
        ]

    def queryset(self, request, queryset):
        if self.value() == QuantityFilter.LESS_THAN_3:
            return queryset.filter(quantity__lt=3)
        elif self.value() == QuantityFilter.BETWEEN_3_AND_10:
            return queryset.filter(quantity__range=(3, 10))
        elif self.value() == QuantityFilter.GREATER_THAN_10:
            return queryset.filter(quantity__gt=10)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product' , 'quantity', 'unit_price']
    ordering = ['id']
    list_per_page = 25
    list_editable = ['unit_price', 'quantity']
    list_select_related = ['order', 'product']
    list_filter = [QuantityFilter]
    search_fields = ['product__name']
    list_display_links = ['id', 'order']
    autocomplete_fields = ['product']
    actions = ['clear_quantity']
    
    @admin.action(description='Clear Quantity')
    def clear_quantity(self, request, queryset):
        update_count = queryset.update(quantity=0)
        self.message_user(request, f"{update_count} quantities of products cleared.", messages.ERROR)


admin.site.register(OrderItem, OrderItemAdmin)



class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name' , 'phone_number', 'birth_date', 'email']
    ordering = ['id']
    list_per_page = 20    
    list_editable = ['birth_date', 'email']
    list_filter = ['orders']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_display_links = ['id', 'first_name']
    
    
admin.site.register(Customer, CustomerAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name' , 'status', 'datetime_created']
    ordering = ['id']
    list_per_page = 20    
    list_editable = ['status']
    list_select_related = ['product']
    list_filter = ['status']
    search_fields = ['product__name']
    list_display_links = ['id', 'product']
    autocomplete_fields = ['product']
    # readonly_fields =
    # fields = 
    # exclude =
    
    
admin.site.register(Comment, CommentAdmin)

