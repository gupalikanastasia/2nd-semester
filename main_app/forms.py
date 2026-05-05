from django import forms
from .models import Subscription, Rating
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Ваше ім'я", 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email', 'class': 'form-control'}),
        }

class PandyRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Введіть дійсну пошту")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(attrs={'class': 'form-select'}),
        }

from .models import Order

class GuestOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': "Ваше ім'я",
                'class': 'form-control',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Номер телефону',
                'class': 'form-control',
                'required': 'required'
            }),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['first_name'].required = True
            self.fields['phone'].required = True