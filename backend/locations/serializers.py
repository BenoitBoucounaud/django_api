from rest_framework import serializers

from .models import City, County, Region


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['code', 'name']


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fileds = ['region', 'code', 'name']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['county', 'code_insee',
                  'code_postal', 'name', 'population', 'area']


class ExtendedRegionSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    name = serializers.CharField()
    totalPopulation = serializers.FloatField()
    totalArea = serializers.FloatField()
    lat = serializers.FloatField()
    lon = serializers.FloatField()
