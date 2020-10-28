from django.shortcuts import render
from django.views.generic import TemplateView

from geo.utils import GeoJSONSerializer
from .models import AccessibleLocal, Rank


# region Frontend
class Dashboard(TemplateView):
    template_name = "geo/index.html"

    def get(self, request, *args, **kwargs):
        ranks = Rank.objects.all()
        args = {
            'ranks': ranks
        }
        return render(request=request, template_name=self.template_name, context=args)


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
