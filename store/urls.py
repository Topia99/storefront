#map our url to view function

from django.urls import path
from . import views

# URLConfiguration
urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.product_detail),
    path('collections/', views.collection_list),
    path('collections/<int:pk>/', views.collection_detail, name="collection_select")
]