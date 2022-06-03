from django import forms
from .models import User


class AddEmployeeForm(forms.ModelForm):
    class Meta:
            model = User
            fields = ('first_name', 'last_name', 'username', 'email')

    def __init__(self, *args, **kwargs):
        super(AddEmployeeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"