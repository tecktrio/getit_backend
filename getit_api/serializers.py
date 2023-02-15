from rest_framework import serializers
from .models import HowToUseDB, LiveDB

from getit_api.models import Users
from getit_api.models import Products

class Users_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('username','password','email','account_type','contact_number','passion','points','subscribers','profile_dp')

class Product_Serailizer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('name','building_name','latitude','longitude','user','rating','upload_date','price','image','description','likes','subcribers','views')

class HowToUse_Serializer(serializers.ModelSerializer):
    class Meta:
        model = HowToUseDB
        fields = ('username','message','show')

class Live_serializer(serializers.ModelSerializer):
    class Meta:
        model = LiveDB
        fields = ('username','title','product','streaming_id','live')