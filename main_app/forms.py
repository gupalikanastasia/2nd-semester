from django import forms
from .models import Subscription, Rating

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Ваше ім'я", 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email', 'class': 'form-control'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(attrs={'class': 'form-select'}),
        }