from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models import Value, F, Func, ExpressionWrapper, Manager
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from store.models import Customer, Collection, Product, OrderItem, Order, Cart, CartItem
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem


# Create your views here.
# request -> response (database)
# request handler

def say_hello(request):
    
    # Create a object
    collection = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1)
    collection.save()
    
    # Update a object
    collection = Collection.objects.get(pk=11)
    collection.featured_product = None
    collection.save()
    
    # Delete a object
    # Delete a collection row which primary key is 11
    collection = Collection(pk=11)
    collection.delete()
    
    # Delete collection which primary key is greater and equal than 5
    Collection.objects.filter(id__gt=5).delete()
    
    # Execise 1
    # Create a shopping cart with an item
    # Create a cart and a cartItem object
    cart = Cart()
    cart.save()
    
    cartItem = CartItem()
    cartItem.cart = cart
    cartItem.product = Product(pk=1)
    cartItem.quantity = 1
    cartItem.save()
    
    # Execise 2
    # Update the quantity of an item in a shopping cart
    cartItem = CartItem.objects.get(pk=CartItem.objects.latest("id"))
    cartItem.quantity = 2
    cartItem.save()
    
    # Execise 3
    # Remove a shopping cart with its items
    cartItem = CartItem.objects.get(pk=CartItem.objects.latest("id"))
    cartItem.delete()

    return render(request, 'hello.html', {'name' : 'Jason', 'tags': list(queryset)})