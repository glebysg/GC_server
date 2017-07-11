from django import forms
from django.forms import ModelForm
from vacs.models import Experiment, Vac
from django.utils.translation import ugettext, ugettext_lazy as _

class ExperimentForm(ModelForm):
    class Meta:
        model = Experiment
        fields = ('name','student_n','expert_n','student_cmd_n',
                'expert_cmd_n','is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                     'id': 'inputName',
                                     'placeholder': 'Experiment Name'}),

            'student_n': forms.NumberInput(attrs={'class': 'form-control',
                                     'id': 'inputStudentN',
                                     'placeholder': 'Number of students'}),

            'expert_n': forms.NumberInput(attrs={'class': 'form-control',
                                     'id': 'inputExpertN',
                                     'placeholder': 'Number of Experts'}),

            'student_cmd_n': forms.NumberInput(attrs={'class': 'form-control',
                                     'id': 'inputStudentN',
                                     'placeholder': 'Number of commands per student'}),

            'expert_cmd_n': forms.NumberInput(attrs={'class': 'form-control',
                                     'id': 'inputExpertCmdN',
                                     'placeholder': 'Number of commands per expert'}),
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



class VacForm(ModelForm):
    class Meta:
        model = Vac
        fields = ('name','description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                     'id': 'inputName',
                                     'placeholder': 'VACs name'}),

            'description': forms.Textarea(attrs={'class': 'form-control',
                                     'id': 'inputDescription',
                                     'placeholder': 'VACs description'}),
        }
