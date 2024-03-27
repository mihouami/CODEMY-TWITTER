from django import forms
from .models import Meep

class MeepForm(forms.ModelForm):
    #meep = forms.CharField(label="", widget=forms.Textarea({'placeholder':'Enter you Meep Here!'}))
    class Meta:
        model = Meep
        fields = ['meep']
        widgets = {
            'meep': forms.Textarea(attrs={'placeholder':'You have something to Meep!'}),
        }
        labels = {
            'meep':'',
        }

    def clean_meep(self):
        meep = self.cleaned_data.get('meep')
        if 'fck' in meep:
            raise forms.ValidationError('Prohibited world in meep!')
        return meep
        

