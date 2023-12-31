from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.aggregates import Count
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from .filters import ProductFilter

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id', 'unit_price']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    # Override destroy method to destroy a object instance
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted becuase it is associated with a product.'},
                            status = status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
class CartViewSet(CreateModelMixin, GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects. \
            filter(cart_id=self.kwargs['cart_pk']). \
                select_related('product')
            

"""

# Use ListAPIView to implement 'post' create object
class ProductList(ListCreateAPIView):
    
    # Use this format if we just want to simply query the object
    '''
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    '''
    
    # GenericAPIView
    def get_queryset(self):
        return Product.objects.all()
    
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

    ''' Do it without using the generic APIView
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    '''
"""

"""
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    #@Override delete method
    def delete(self, request, pk):
        # Get Product object from db with id
        product = get_object_or_404(Product, pk=pk)
        
        # Check related field
        if product.orderitems.count() > 0: # If this product has a foregin key in orderitem
            # Return a Error message
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Delete product
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
        
'''
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    
    def patch(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()   
        
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'}, 
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        Product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''


''' The basic way to do it Product_List
# Create your views here.
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PATCH', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':         
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()   
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'}, 
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
'''
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
'''

''' Implement it in a logic way, more basic collection_list
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products'))
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
'''
'''
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    
    # Override delete method because it require to check associated table
    def delete(self, request, pk):
        # Get Product object from db with id
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be delete because it is associated with products'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''

''' collection_detial
@api_view(['GET', 'PATCH', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count('products')), 
        pk=pk
    )
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        # Check whether delete object associated with other table
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be delete because it is associated with products'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
    