# scripts/imports.py

import pandas as pd
from locations.models import City, County, Region


def run():
    locations_csv_to_db()


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
