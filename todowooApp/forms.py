from django.forms import ModelForm
from .models import todowooApp

class todowooAppForm(ModelForm):
    class Meta:
        model = todowooApp
        fields = ['title', 'memo', 'important']
