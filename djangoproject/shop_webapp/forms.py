from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserInfoForm(forms.ModelForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), required=True)
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), required=True)
    first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), required=True)
    last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), required=True)
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}), required=False)
    address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}), required=False)
    address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}), required=False)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}), required=False)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address1', 'address2', 'city', 'state', 'country', 'zipcode']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['username'].initial = user.username
        self.fields['email'].initial = user.email
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['phone'].initial = self.instance.phone
        self.fields['address1'].initial = self.instance.address1
        self.fields['address2'].initial = self.instance.address2
        self.fields['city'].initial = self.instance.city
        self.fields['state'].initial = self.instance.state
        self.fields['country'].initial = self.instance.country
        self.fields['zipcode'].initial = self.instance.zipcode

    def save(self, commit=True):
        user_instance = super(UserInfoForm, self).save(commit=False)
        user = User.objects.get(pk=user_instance.user.id)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user_instance.phone = self.cleaned_data['phone']
        user_instance.address1 = self.cleaned_data['address1']
        user_instance.address2 = self.cleaned_data['address2']
        user_instance.city = self.cleaned_data['city']
        user_instance.state = self.cleaned_data['state']
        user_instance.country = self.cleaned_data['country']
        user_instance.zipcode = self.cleaned_data['zipcode']
        if commit:
            user.save()
            user_instance.save()
        return user_instance
