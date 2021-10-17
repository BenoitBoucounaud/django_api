from django.db import models


class Region(models.Model):
    code = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return super().__str__()


class County(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return super().__str__()


class City(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    code_insee = models.CharField(max_length=10, unique=True)
    code_postal = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    population = models.FloatField()
    area = models.FloatField()

    def __str__(self) -> str:
        return super().__str__()
