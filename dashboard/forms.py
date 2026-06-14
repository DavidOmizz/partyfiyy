from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django.forms import ModelForm
from .models import Testimonial

class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label = 'username', widget= forms.TextInput(attrs={'placeholder':'Username', 'class': 'form-control'}))
    password = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))



class TestimonialForm(ModelForm):
        client_name = forms.CharField(label = 'name', widget= forms.TextInput(attrs={'placeholder':'Enter full name', 'class': 'form-control'}))
        client_title = forms.CharField(label = 'title', widget= forms.TextInput(attrs={'placeholder':'Enter title', 'class': 'form-control'}))
        client_company = forms.CharField(label = 'company', widget= forms.TextInput(attrs={'placeholder':'Enter Company Name', 'class': 'form-control'}))
        client_image = forms.URLField(label = 'image', widget= forms.URLInput(attrs={'placeholder':'Enter image URL', 'class': 'form-control'}))
        content = forms.CharField(label = 'content', widget= forms.Textarea(attrs={'placeholder':'Message', 'class': 'form-control'}))
        rating = forms.IntegerField(label = 'rating', widget= forms.NumberInput(attrs={'placeholder':'Rating', 'class': 'form-control'}))

        class Meta:
            model = Testimonial
            fields = ('client_name', 'rating', 'content', 'client_company')