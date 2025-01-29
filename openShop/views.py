from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from openShop.serializers import ProductSerializer
from .models import Product
from django.http import Http404

# Create your views here.
class ProductList(APIView):
    def post(self, request):
        product = ProductSerializer(data=request.data, context={'request':request})
        if product.is_valid(raise_exception=True):
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        return Response(product.error, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        name = request.GET.get('name', None)
        location = request.GET.get('location', None)

        product = Product.objects.all()

        if name:
            product = product.filter(name__icontains=name)

        if location:
            product = product.filter(location__icontains=location)

        serializer = ProductSerializer(product, many=True, context={'request':request})
        return Response({
            "products": serializer.data
        }, status=status.HTTP_200_OK)
    

class ProductDetail(APIView):
    def get_object(self,pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self, request,pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data = request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.is_delete = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)