from django import forms

from django.contrib.auth.models import User

from django.core.validators import validate_email,RegexValidator

from grumblr.models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20,
                               validators = [RegexValidator(r'^[0-9a-zA-Z]*$',
                               message='Username can only contain letters and numbers')])
    last_name = forms.CharField(max_length = 20, label = 'Last name')
    first_name = forms.CharField(max_length = 20, label = 'First name')
    email = forms.CharField(max_length = 80, label = 'E-mail',validators = [validate_email])
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput())
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

class ProfileForm(forms.ModelForm):
    password = forms.CharField(label='New password',widget = forms.PasswordInput(),required=False)
    class Meta:
        model = Profile 
        exclude = ('owner', 'follow',)
        widgets = {'photo':forms.FileInput()}

class Reset_password(forms.Form):
    username = forms.CharField(max_length = 20,
                               validators = [RegexValidator(r'^[0-9a-zA-Z]*$',
                               message='Username can only contain letters and numbers')])

    def clean(self):
        cleaned_data = super(Reset_password, self).clean()
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username does not exist.")
        return username

class Reset_password_form2(forms.Form):
    password = forms.CharField(max_length = 200, 
                                label='New Password', 
                                widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super(Reset_password_form2, self).clean()
        return cleaned_data

class Blog_form(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['text']

class Comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
