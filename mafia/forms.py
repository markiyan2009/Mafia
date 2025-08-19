from django import forms
from .models import *

class CreateGamerForm(forms.ModelForm):
    class Meta:
        model = Gamers
        fields = ['name']
        widget = {
            'name' : forms.TextInput(attrs={'class':'form-control'})
        }
GamersFormSet = forms.modelformset_factory(Gamers, CreateGamerForm, extra=4, can_delete=True)
    
class UpdateRoleForm(forms.Form):
    gamer = forms.ModelChoiceField(queryset=Gamers.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gamer'].queryset = Gamers.objects.all()

SetRoleFormSet = forms.formset_factory(UpdateRoleForm, extra=1, can_delete=True)

