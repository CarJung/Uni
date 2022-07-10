from django import forms
from django.forms import fields
from .models import KWarticles, KWComment

class KWarticleForm(forms.ModelForm):

    class Meta:
        model = KWarticles
        fields = ['title','description','content','pub_user']



class ComentForm(forms.ModelForm):

    class Meta:
        model = KWComment
        fields = ['user','comment']

class KontaktForm(forms.Form):
    first_name = forms.CharField(max_length = 50, label ='Imie')
    last_name = forms.CharField(max_length = 50, label ='Nazwisko')
    c_mail = forms.EmailField(max_length = 50, label ='Mail')
    text = forms.CharField(widget =forms.Textarea, max_length= 1000, label ='Treść')