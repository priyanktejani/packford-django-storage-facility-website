from django import forms
from .models import Item


class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category']

    def __init__(self, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        # self.fields['category'].widget.attrs['placeholder'] = 'Item category must match the crate category'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"