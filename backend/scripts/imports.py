# scripts/imports.py

import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.indexes.base import Index
from locations.models import City, County, Region
import requests

OUTPUT_DIR = 'backend/resources'


def run(*args):
    if 'csv_to_db' in args:
        locations_csv_to_db()

    if 'osm_data' in args:
        osm_to_csv()


def locations_csv_to_db():

    locations = pd.read_csv(
        'backend/resources/french_pcs.csv', sep=';')

    regions = []
    counties = []
    cities = []

    # Unique lists, check if code or code_insee are not duplicate
    regions_unique = []
    counties_unique = []
    cities_unique = []

    for index, row in locations.iterrows():

        region = Region(
            code=row["Code Région"],
            name=row["Région"]
        )
        # check if already exists and add to array else assign the already existed region
        # permit to link the real region to the county
        if region.code not in regions_unique:
            regions_unique.append(region.code)
            regions.append(region)
        else:
            region = next(r for r in regions if r.code == region.code)

        county = County(
            region=region,
            code=row["Code Département"],
            name=row["Département"]
        )
        # check if already exists and add to array else assign the already existed county
        # permit to link the real county to the city
        if county.code not in counties_unique:
            counties_unique.append(county.code)
            counties.append(county)
        else:
            county = next(c for c in counties if c.code == county.code)

        city = City(
            county=county,
            code_insee=row["Code INSEE"],
            code_postal=row["Code Postal"],
            name=row["Commune"],
            population=row["Population"],
            area=row["Superficie"]
        )
        if city.code_insee not in cities_unique:
            cities_unique.append(city.code_insee)
            cities.append(city)

    Region.objects.bulk_create(regions)

    for county in counties:
        county.region_id = county.region.id

    County.objects.bulk_create(counties)

    for city in cities:
        city.county_id = city.county.id

    City.objects.bulk_create(cities)


def osm_to_csv():
    '''
    Use nominatim for lat and lon
    https://nominatim.org/release-docs/develop/api/Search/
    This API is very slow (read here max 1 query/sec https://operations.osmfoundation.org/policies/nominatim/)

    We admit every entries are in France
    '''

    regions = Region.objects.all()
    regions_list = []

    for r in regions:
        url = "https://nominatim.openstreetmap.org/search?country=France&state=%s&format=json" % (
            r.name)
        data = requests.get(url)
        data = data.json()

        if len(data) == 1:
            region = {
                'region': r.name,
                'lat': data[0]['lat'],
                'lon': data[0]['lon']
            }
            regions_list.append(region)
        else:
            print('%s not found' % (r.name))

    df = pd.DataFrame(regions_list, columns=['region', 'lat', 'lon'])
    df.to_csv('backend/resources/osm_data.csv', index=False, encoding='utf-8')
