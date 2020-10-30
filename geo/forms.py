from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div
from django.contrib.gis import forms
from django.forms.widgets import Textarea
from django.contrib.auth.forms import UserCreationForm

from geo.models import AccessibleLocal, User


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
            Submit('save', 'Salvar', css_class='btn-success')
        )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'email': 'Endereço de email',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'password1': 'Senha',
            'password2': 'Confirmar senha',
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'signup'
        self.helper.form_method = 'post'
        self.helper.form_action = 'signup'
        self.helper.add_input(Submit('save', 'Cadastrar', css_class='btn-success'))
