import requests
from django.db.models.aggregates import Sum
from django.db.models.expressions import Value
from django.db.models.fields import FloatField
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Region
from .serializers import ExtendedRegionSerializer

paginator = PageNumberPagination()
paginator.page_size = 10


@api_view(['GET'])
def region_list(request):
    """
    More details on api_view :
    https://www.django-rest-framework.org/tutorial/2-requests-and-responses/#wrapping-api-views

    List all regions
    """
    if request.method == 'GET':
        regions = Region.objects.annotate(
            totalPopulation=Sum('county__city__population'),
            totalArea=Sum('county__city__area'),
            lat=Value(0, output_field=FloatField()),
            lon=Value(0, output_field=FloatField())
        )

        # add lat and long
        for region in regions:
            osm = getOSMData(region.name)
            if len(osm) == 1:
                region.lat = osm[0]['lon']
                region.lon = osm[0]['lat']
            else:
                print('%s not found' % (region.name))

        result_page = paginator.paginate_queryset(regions, request)
        serializer = ExtendedRegionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        serializer = ExtendedRegionSerializer()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def getOSMData(region):
    '''
    Use nominatim for lat and lon
    https://nominatim.org/release-docs/develop/api/Search/
    This API is very slow (read here max 1 query/sec https://operations.osmfoundation.org/policies/nominatim/)
    I didnt found a way to make one big query to catch every states

    We admit every entries are in France
    '''
    url = "https://nominatim.openstreetmap.org/search?country=France&state=%s&format=json" % (
        region)
    data = requests.get(url)
    return data.json()
