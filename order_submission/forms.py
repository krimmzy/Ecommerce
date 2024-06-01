from django import forms

class ShippingForm(forms.Form):
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	address = forms.CharField(max_length=1000)
	email = forms.EmailField()
	phone_number = forms.CharField(max_length=20)
	city = forms.CharField(max_length=100)
	state = forms.CharField(max_length=100)
	country = forms.CharField(max_length=100)