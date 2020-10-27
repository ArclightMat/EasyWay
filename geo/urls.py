from django.urls import path
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='index'),
    path('about/', views.About.as_view(), name='about'),
    path('login/', views.Login.as_view(), name='login'),
    path('api/locals', views.AccessibleLocalGeoJSONList.as_view(), name='api_list_locals')
]
