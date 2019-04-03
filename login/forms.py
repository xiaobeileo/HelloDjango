from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='ConfirmCode')


class RegisterForm(forms.Form):
    gender = (
        ('male', "M"),
        ('female', "F"),

    )

    username = forms.CharField(label='UserName', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password_first = forms.CharField(label="Password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_second= forms.CharField(label="confirm", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email Addr", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='Sex', choices=gender)
    captcha = CaptchaField(label='Captcha')