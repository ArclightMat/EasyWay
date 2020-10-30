from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import HttpResponse
from django.views.generic import View
from django.core.serializers import serialize
from rest_framework import serializers

from geo.models import User


class GeoJSONSerializer(View):
    """
    A replacement for Django REST Framework GIS, since it is not working with Django 3.1 + Django REST Framework 3.12
    :param model: A model with GeoDjango fields
    :param geometru_field: A GeoDjango field to be used as the 'geometry' value
    :param fields: Optional, tuple of model fields to be serialized
    """
    model: Model = None
    geometry_field: str = None
    fields: tuple = None

    def get(self, request, *args, **kwargs):
        assert self.model is not None
        assert self.geometry_field is not None
        key = kwargs.get('id', None)
        if self.fields is None:
            if key is not None:
                data = serialize('geojson', self.model.objects.filter(id=key), geometry_field=self.geometry_field,
                                 fields=self.fields)
            else:
                data = serialize('geojson', self.model.objects.filter(is_active=True),
                                 geometry_field=self.geometry_field,
                                 fields=self.fields)
        else:
            if key is not None:
                data = serialize('geojson', self.model.objects.filter(id=key), geometry_field=self.geometry_field)
            else:
                data = serialize('geojson', self.model.objects.filter(is_active=True),
                                 geometry_field=self.geometry_field)
        return HttpResponse(data, content_type='application/json')

    def post(self, request, *args, **kwargs):
        # Creation is being done with Forms
        return HttpResponse(status=404)

    def patch(self, request, *args, **kwargs):
        # Editing is being done with Forms
        return HttpResponse(status=404)

    @login_required
    def delete(self, request, *args, **kwargs):
        key = kwargs.get('id', None)
        if key is not None:
            data = self.model.objects.get(id=key)
            data.is_active = False
            data.save()
        return HttpResponse(status=204)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'show_alerts']
        read_only_fields = ['id']
