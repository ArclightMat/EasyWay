from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework.generics import RetrieveUpdateAPIView

from geo.utils import GeoJSONSerializer, UserSerializer
from .forms import AccessibleLocalForm, RegisterForm
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
                                                       created_by=request.user)
            else:
                entry = AccessibleLocal.objects.get(id=key)
                entry.name = form.cleaned_data['name']
                entry.comments = form.cleaned_data['comments']
                entry.location = location
                entry.rank = form.cleaned_data['rank']
            entry.save()
            return redirect('index')
        args = {
            'form': form
        }
        return render(request=request, template_name=self.template_name, context=args)


class Register(TemplateView):
    template_name = "registration/signup.html"
    form = RegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        args = {
            'form': form
        }
        return render(request=request, template_name=self.template_name, context=args)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('index')
        args = {
            'form': form
        }
        return render(request=request, template_name=self.template_name, context=args)


class About(TemplateView):
    template_name = "geo/about.html"


class Help(TemplateView):
    template_name = "geo/help.html"


# endregion

# region APIs
class AccessibleLocalGeoJSONList(GeoJSONSerializer):
    model = AccessibleLocal
    geometry_field = 'location'
    fields = ('name', 'comment', 'rank')


class UserSerializerController(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = serializer_class.Meta.model.objects.filter(is_active=True)
# endregion
