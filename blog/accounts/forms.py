from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, login, logout,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .models import UserProfile



class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")


        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, label='Email address')
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=25,label='First name')
    last_name = forms.CharField(max_length=25, label='Last name')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password1',
        ]

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if len(username) < 1:
            raise forms.ValidationError("Enter username!")
        else:
            user_exist = User.objects.filter(username__iexact=username).exists()
            if user_exist:
                raise forms.ValidationError("Username already taken!")
            else:
                if len(email) < 1:
                    raise forms.ValidationError("Enter email address!")
                else:
                    if len(password1) < 8:
                        raise forms.ValidationError("Password is too short!")
                    else:
                        if password1 != password2:
                            raise forms.ValidationError("Password not matched!")



class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
        ]

class ChangeBasicInfo(forms.ModelForm):
    description = forms.CharField(max_length=400, label='Description',required=False)
    city = forms.CharField(max_length=100, required=False)
    website = forms.URLField(required=False)
    phone = forms.CharField(max_length=18, required=False)
    image = forms.ImageField(required=False)


    class Meta:
        model = UserProfile
        fields = [
            'description',
            'city',
            'website',
            'phone',
            'image'
        ]

    def clean(self):
        description = self.cleaned_data.get("description")
        city = self.cleaned_data.get("city")
        website = self.cleaned_data.get("website")
        phone = self.cleaned_data.get("phone")
        image = self.cleaned_data.get("image")



class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', max_length=20, required=False, widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', max_length=20, required=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm Password', max_length=20, required=False, widget=forms.PasswordInput)

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
