from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='index'),
    path('api/locals', views.AccessibleLocalGeoJSONList.as_view(), name='api_list_locals')
]
