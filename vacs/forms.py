from django import forms
from django.forms import ModelForm
from vacs.models import Experiment, Vac, Evaluation, Validation
from django.utils.translation import ugettext, ugettext_lazy as _
import re

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
        elif command_number > 84:
            raise forms.ValidationError(
                "The total number of commands to be evaluated must be less than 85"
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

class EvaluationForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ('evaluation',)

    def clean(self):
        cleaned_data = super(EvaluationForm, self).clean()
        evaluation = cleaned_data.get("evaluation")
        match = re.search('^(([1-9]\.(=|<)\.[1-9]\.(=|<)\.[1-9])|empty)$',evaluation)
        if not match:
            raise forms.ValidationError(
                "Please make sure that you have one video in each of the boxes"
            )
        return self.cleaned_data


class ValidationForm(ModelForm):
    class Meta:
        model = Validation
        fields = ('selected_lexicons',)

    def clean(self):
        cleaned_data = super(ValidationForm, self).clean()
        selected_lexicons = cleaned_data.get("selected_lexicons")
        match = re.search('^(([1-9]\.)+|empty)$',selected_lexicons)
        if not match:
            raise forms.ValidationError(
                "Please make sure that you selected a video"
            )
        return self.cleaned_data
