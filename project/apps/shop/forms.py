from django import forms
from django import forms


class OrderCreateForm(forms.Form):
    full_name = forms.CharField(required=True, max_length=150)
    phone = forms.CharField(required=True, max_length=25)
    email = forms.CharField(required=True, max_length=100)
    comment = forms.Textarea()
