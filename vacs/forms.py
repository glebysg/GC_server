from django import forms

class ExperimentForm(forms.Form):
    name = forms.CharField(max_length=254,
            widget=forms.TextInput(attrs={'class': 'form-control',
                                          'id': 'inputName',
                                          'placeholder': "Experiment Name"}))
    student_n = forms.IntegerField()
    expert_n = forms.IntegerField()
    student_cmd_n = forms.IntegerField()
    expert_cmd_n = forms.IntegerField()
    is_active = forms.BooleanField()

    def clean(self):
        cleaned_data = super(ExperimentForm, self).clean()
        s_n = cleaned_data.get("student_n")
        e_n = cleaned_data.get("expert_n")
        s_cmd_n = cleaned_data.get("student_cmd_n")
        e_cmd_n = cleaned_data.get("expert_cmd_n")
        command_number = s_n*s_cmd_n + e_n*e_cmd_n
        if command_number < 28:
            msg = "The total number of commands to be evaluated must be\
                  Greater than 28. Right now it's" + str(command_number)
            self.add_error('student_n', msg)
            self.add_error('expert_n', msg)
