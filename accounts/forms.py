from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists(): raise forms.ValidationError('An account already uses this email.')
        return email

class UserForm(forms.ModelForm):
    class Meta: model = User; fields = ('username','email','first_name','last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile; fields = ('profile_picture','bio'); widgets = {'bio': forms.Textarea(attrs={'rows': 5})}
    def clean_profile_picture(self):
        image = self.cleaned_data.get('profile_picture')
        if image and image.size > 3 * 1024 * 1024: raise forms.ValidationError('Profile image must be 3 MB or smaller.')
        return image
