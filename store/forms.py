from django import forms
from django.contrib.auth.models import User
from .models import Comment, Staff
from django.core.exceptions import ValidationError


class AddComment(forms.ModelForm):
    text = forms.CharField(
        label='Текст комментария',
        max_length=800,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'rows': '3'})
    )

    class Meta:
        model = Comment
        fields = ['text']


class UserLogin(forms.Form):
    login = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
    )

    class Meta:
        fields = ['login', 'password', ]


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
        max_length=50
    )

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'password', 'confirm_password', ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(unique_username_validator)
        self.fields['username'].validators.append(username_validator)
        self.fields['email'].validators.append(unique_email_validator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Passwords don\'t match'])
            return self.cleaned_data


def username_validator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Username contains forbidden symbols.')


def unique_username_validator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('Username is not unique.')


def unique_email_validator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('Email is not unique.')
