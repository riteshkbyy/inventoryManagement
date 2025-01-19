from django import forms

class SupplierForm(forms.Form):
    name = forms.CharField(max_length=255)
    contact_email = forms.EmailField()
    contact_phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
