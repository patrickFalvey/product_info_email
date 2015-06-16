from django import forms

class product_info_email_form(forms.Form):
    Customer_email = forms.EmailField()
