from django import forms
from .models import Meep
from crispy_forms.helper import FormHelper
from django.urls import reverse_lazy


class MeepForm(forms.ModelForm):
    """
    #meep = forms.CharField(required=True,
                            label="",
                            widget=forms.Textarea({'placeholder':'Enter you Meep Here!',
                                                   'class':'form-control}))
    """

    class Meta:
        model = Meep
        fields = ["meep"]
        unique_together=('meep')
        widgets = {
            "meep": forms.Textarea(
                attrs={
                    "placeholder": "You have something to Meep!",
                    'hx-get':reverse_lazy('check_meep'),
                    'hx-trigger':'keyup change',
                    'hx-target':'#div_id_meep',
                    'hx-swap':'outerHTML',
                    }
            ),
        }
        
        labels = {
            "meep": "",
        }

    def clean_meep(self):
        meep = self.cleaned_data.get("meep")
        if "fck" in meep.split():
            raise forms.ValidationError("Prohibited world in meep!")
        return meep
