from django.forms.models import ModelForm
from clktc.links.models import Link

class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ('short_url', 'destination_url')
