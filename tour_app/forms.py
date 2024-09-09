from django import forms
from django.contrib.auth import get_user_model
from .models import Tour


User = get_user_model()

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']  # Include additional fields if necessary

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
class TourUpdateForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['place_name', 'weather', 'location_state', 'location_district', 'google_map_link', 'image', 'description']



class AddDestinationForm(forms.ModelForm):
    class Meta:
        model = Tour
        fields = ['place_name', 'weather', 'location_state', 'location_district', 'google_map_link', 'image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class LogoutForm(forms.Form):
    refresh = forms.CharField(widget=forms.HiddenInput())

