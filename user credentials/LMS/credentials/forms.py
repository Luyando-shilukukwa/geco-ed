from django import forms
from .models import Tutor



class TutorForm(forms.ModelForm):
     class meta:
         model = Tutor
         fields = ['name', 'email', 'mobile_number']
