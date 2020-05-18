from django.forms import ModelForm
from .models import Manager

class ManagerForm(ModelForm):
    class Meta:
        model = Manager
        fields = ('username','mobile','email')
