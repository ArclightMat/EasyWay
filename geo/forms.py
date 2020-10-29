from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div
from django.contrib.gis import forms
from django.forms.widgets import Textarea

from geo.models import AccessibleLocal


class AccessibleLocalForm(forms.ModelForm):
    lat = forms.FloatField(required=True, min_value=-90, max_value=90)  # Latitude: -90° to 90°
    lng = forms.FloatField(required=True, min_value=-180, max_value=180)  # Longitude: -180° to 180°

    class Meta:
        model = AccessibleLocal
        fields = ['name', 'comments', 'lat', 'lng', 'rank']
        labels = {
            'name': 'Nome do local:',
            'comments': 'Descrição do local:',
            'rank': 'Nível de Acessibilidade:',
        }
        widgets = {
            'comments': Textarea()
        }

    def __init__(self, *args, **kwargs):
        super(AccessibleLocalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'manage_local'
        self.helper.form_method = 'post'
        self.helper.form_action = 'index'
        self.helper.layout = Layout(
            Field('name', id='name'),
            Field('comments', id='comments', rows=3),
            Field('rank', id='rank'),
            Div(Field('lat', type='hidden', id='lat'),
                Field('lng', type='hidden', id='lon'),
                id='div_id_coords'
                ),
            Submit('criar', 'Criar', css_class='btn-success')
        )
