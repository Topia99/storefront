# Register your models here.
from typing import Any
from django.contrib import admin
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from . import models

# Register Product model, and define the column to display
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection'] # Load the collection table ahead so the collection_title does query on the collection table repeatedly
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory') # Allow sort in inventory column
    def inventory_status(self, product):    # Function to return inventory status base on its inventory
        if product.inventory < 10:
            return 'low'
        return 'ok'
    
# Register Customer model
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    
# Register Order model. Be able to see the customer of the order
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    
    
    

# Register Collection table in the admin
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )