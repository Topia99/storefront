from django.contrib import admin
from django.db import models
from django.conf import settings

# Promotion(s) - Product(s)
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    
    

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    # Change the admin object's name to its title 
    def __str__(self) -> str:
        return self.title
    # Sort in ascending order
    class Meta:
        ordering = ["title"]

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField() 
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # products - collection
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    #promotion
    promotions = models.ManyToManyField(Promotion, blank=True)
    # Change the admin object name to its title
    def __str__(self)  -> str:
        return self.title
    class Meta:
        ordering = ['title']


class Customer(models.Model):
    MEMBERSHIP_BROZE = 'B'
    MEMBERSHIP_SLIVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BROZE, 'Bronze'),
        (MEMBERSHIP_SLIVER, 'Sliver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BROZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   
    # Change the admin object name to its first + last name
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        
    
class Order(models.Model):
    
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    ]
    
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)
    # Orders - Customer
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    
    
    
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=5)
    # Customer - Address
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField() 