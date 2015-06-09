from django import forms

class ProductInfoEmailForm(forms.Form):
    Customer_email = forms.EmailField()
