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


from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

def validate_card_number(value):
    if not value.isdigit() or len(value) != 16:
        raise ValidationError("Номер карты должен состоять из 16 цифр.")

def validate_cvc(value):
    if not value.isdigit() or len(value) != 3:
        raise ValidationError("CVC код должен состоять из 3 цифр.")

class PaymentForm(forms.ModelForm):
    card_number = forms.CharField(
        validators=[validate_card_number],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Номер карты',
                'autocomplete': 'cc-number',
                'maxlength': '16',
                'minlength': '16',
            }
        )
    )
    cvc = forms.CharField(
        validators=[validate_cvc],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'CVC',
                'autocomplete': 'cc-csc',
                'maxlength': '3',
                'minlength': '3',
            }
        )
    )

    class Meta:
        model = Payment
        fields = ['card_number', 'cvc']
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


