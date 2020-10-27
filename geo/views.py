from django.views.generic import TemplateView

from geo.utils import GeoJSONSerializer
from .models import AccessibleLocal


class Dashboard(TemplateView):
    template_name = "gate/index.html"


class AccessibleLocalGeoJSONList(GeoJSONSerializer):
    model = AccessibleLocal
    geometry_field = 'location'
    fields = ('name', 'comment', 'rank')
