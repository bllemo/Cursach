from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        label="ФИО",
        widget=forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'})
    )
    username = forms.CharField(
        max_length=30,
        label="Логин",
        widget=forms.TextInput(attrs={'placeholder': 'ivan_ivanov'})
    )
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Повтор пароля"
    )
    consent = forms.BooleanField(
        label="Согласие на обработку персональных данных",
        error_messages={'required': 'Вы должны согласиться на обработку ПД.'}
    )

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', full_name):
            raise ValidationError("ФИО может содержать только кириллические буквы, пробелы и дефисы.")
        return full_name.strip()

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9\-]+$', username):
            raise ValidationError("Логин может содержать только латинские буквы, цифры и дефис.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2