from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, min_length=3,)
    last_name = forms.CharField(required=True, min_length=3,)

    class Meta:
        model = User
        fields = (
            'email','username', 'password1', 'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('first_name', None)
        self.fields.pop('last_name', None)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_instance = self.instance

        if user_instance and user_instance.email == email:
            return email

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Este email já está em uso', code='invalid')
            )
        return email
