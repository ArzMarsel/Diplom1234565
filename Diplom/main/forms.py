from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MinLengthValidator, MinValueValidator, MaxLengthValidator
from django_recaptcha.fields import ReCaptchaField
from .models import Payment, Connect


class UserCreation(UserCreationForm):
    # captcha = ReCaptchaField()
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password 1'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password 2'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', ]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'password1']


class PaymentForm(forms.ModelForm):
    card_number = forms.IntegerField(
        validators=[MaxLengthValidator(16), MinLengthValidator(16)],

        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Номер карты'
            }
        )
    )
    cvc = forms.IntegerField(
        validators=[MinLengthValidator(3), MinLengthValidator(3)],
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'CVC'
            }
        )
    )

    class Meta:
        model = Payment
        fields = ['card_number', 'cvc']
        widgets = {
            'card_number': forms.TextInput(attrs={'placeholder': 'Номер карты', 'autocomplete': 'cc-number'}),
            'cvc': forms.TextInput(attrs={'placeholder': 'CVC', 'autocomplete': 'cc-csc'}),
        }


class ConnectForm(forms.ModelForm):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Кол-во'
            }
        )
    )

    class Meta:
        model = Connect
        fields = ['quantity']


