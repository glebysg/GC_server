from django import forms
from django.forms import ModelForm
from vacs.models import Experiment
from django.utils.translation import ugettext, ugettext_lazy as _

class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        fields = ('name','student_n','expert_n','student_cmd_n',
                'expert_cmd_n','is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                     'id': 'inputName',
                                     'placeholder': 'Experiment Name'})
        }

    def clean(self):
        cleaned_data = super(ExperimentForm, self).clean()
        s_n = cleaned_data.get("student_n")
        e_n = cleaned_data.get("expert_n")
        s_cmd_n = cleaned_data.get("student_cmd_n")
        e_cmd_n = cleaned_data.get("expert_cmd_n")
        command_number = s_n*s_cmd_n + e_n*e_cmd_n
        if command_number < 28:
            raise forms.ValidationError(
                "The total number of commands to be evaluated must be greater than 28"
            )
        return self.cleaned_data
