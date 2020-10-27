from django.views.generic import TemplateView

from geo.utils import GeoJSONSerializer
from .models import AccessibleLocal


# region Frontend
class Dashboard(TemplateView):
    template_name = "geo/index.html"


class About(TemplateView):
    template_name = "geo/about.html"


class Login(TemplateView):
    template_name = "geo/login.html"


# endregion

# region APIs
class AccessibleLocalGeoJSONList(GeoJSONSerializer):
    model = AccessibleLocal
    geometry_field = 'location'
    fields = ('name', 'comment', 'rank')
# endregion
