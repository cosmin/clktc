from django.forms import forms
from django.forms.models import ModelForm
from clktc.bootstrap.forms import BootstrapModelForm
from clktc.links.models import Link

class AddLinkForm(BootstrapModelForm):
    class Meta:
        model = Link
        fields = ('short_url', 'destination_url', 'site')
        widgets = {
            'destination_url': forms.TextInput,
            'short_url': forms.TextInput,
        }

class EditLinkForm(AddLinkForm):
    class Meta:
        model = Link
        fields = ['destination_url']
        widgets = {
            'destination_url': forms.TextInput,
        }
