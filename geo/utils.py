from django.db.models import Model
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.core.serializers import serialize


class GeoJSONSerializer(View):
    """
    A replacement for Django REST Framework GIS, since it is not working with Django 3.1 + Django REST Framework 3.12
    :param model: A model with GeoDjango fields
    :param geometru_field: A GeoDjango field type
    :param fields: Optional, tuple of model fields to be serialized
    """
    model: Model = None
    geometry_field: str = None
    fields: tuple = None

    def get(self, request, *args, **kwargs):
        assert self.model is not None
        assert self.geometry_field is not None
        if self.fields is None:
            data = serialize('geojson', self.model.objects.all(), geometry_field=self.geometry_field,
                             fields=self.fields)
        else:
            data = serialize('geojson', self.model.objects.all(), geometry_field=self.geometry_field)
        return HttpResponse(data, content_type='application/json')

    def post(self, request, *args, **kwargs):
        pass
