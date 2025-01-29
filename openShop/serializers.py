from rest_framework import serializers
from openShop.models import Product

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','shop','price','sku','description','location','discount','category','stock','is_available','picture']