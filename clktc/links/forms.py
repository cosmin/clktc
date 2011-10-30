from django.forms import forms
from django.forms.models import ModelForm
from clktc.bootstrap.forms import BootstrapModelForm
from clktc.links.models import Link

class LinkForm(BootstrapModelForm):
    class Meta:
        model = Link
        fields = ('short_url', 'destination_url')
        widgets = {
            'destination_url': forms.TextInput,
            'short_url': forms.TextInput,
        }
