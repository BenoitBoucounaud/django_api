from django.urls import path

from locations import views

app_name = 'locations'

urlpatterns = [
    path('regions/', views.region_list, name='region-list'),
]
