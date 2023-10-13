#map our url to view function

from django.urls import path
from . import views

# URLConfiguration
urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail)
]