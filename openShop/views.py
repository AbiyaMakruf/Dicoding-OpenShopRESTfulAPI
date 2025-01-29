from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from openShop.serializers import ProductSerializer
from .models import Product

# Create your views here.
class ProductList(APIView):
    def post(self, request):
        product = ProductSerializer(data=request.data, context={'request':request})
        if product.is_valid(raise_exception=True):
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        return Response(product.error, status=status.HTTP_400_BAD_REQUEST)