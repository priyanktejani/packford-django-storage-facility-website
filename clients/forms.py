from django import forms
from .models import Company, Branch, Location 

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name']


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['branch_name']

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        self.fields['branch_name'].widget.attrs['placeholder'] = 'Branch_name'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"