import pandas as pd
from pandas.io import json
import requests
from django.db.models.aggregates import Sum
from django.db.models.expressions import Value
from django.db.models.fields import FloatField
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

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


def getOSMData(region_name):
    """
    Need to build/update osm_data.csv first with ./run.sh osm_data 
    """
    df = pd.read_csv('backend/resources/osm_data.csv', sep=',')
    data = df.loc[df['region'] == region_name]
    result = data.to_json(orient="records")
    return json.loads(result)
