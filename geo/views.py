from django.contrib.gis.geos import Point
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from geo.utils import GeoJSONSerializer
from .forms import AccessibleLocalForm
from .models import AccessibleLocal


# region Frontend
class Dashboard(TemplateView):
    template_name = "geo/index.html"
    form = AccessibleLocalForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        args = {
            'form': form
        }
        return render(request=request, template_name=self.template_name, context=args)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        key = self.kwargs.get('id', None)
        if form.is_valid():
            # Point: first is longitude, second is latitude.
            location = Point(form.cleaned_data['lng'], form.cleaned_data['lat'])
            if key is None:
                entry = AccessibleLocal.objects.create(name=form.cleaned_data['name'],
                                                       comments=form.cleaned_data['comments'],
                                                       location=location,
                                                       rank=form.cleaned_data['rank'],
                                                       created_by_id=1)  # TODO: Placeholder value, replace with User
            else:
                entry = AccessibleLocal.objects.get(id=key)
                entry.name = form.cleaned_data['name']
                entry.comments=form.cleaned_data['comments']
                entry.location = location
                entry.rank = form.cleaned_data['rank']
            entry.save()
            return redirect('index')
        args = {
            'form': form
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
