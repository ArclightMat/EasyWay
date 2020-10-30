from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Dashboard.as_view(), name='index'),
    path('about/', views.About.as_view(), name='about'),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
    path('help/', views.Help.as_view(), name='help'),
    path('api/locals', views.AccessibleLocalGeoJSONList.as_view(), name='api_list_locals'),
    path('api/locals/<int:id>', views.AccessibleLocalGeoJSONList.as_view(), name='api_details_locals'),
    path('api/edit_local/<int:id>', views.Dashboard.as_view(), name='edit'),
    path('api/user/<int:pk>', views.UserSerializerController.as_view(), name='api_update_user'),
]
