from django import forms

from .models import Profile


class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}), required=False)
    address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}), required=False)
    address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}), required=False)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}), required=False)

    class Meta:
        model = Profile
        fields = ['phone', 'address1', 'address2', 'city', 'state', 'country', 'zipcode']
