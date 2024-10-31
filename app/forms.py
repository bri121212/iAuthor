from django import forms

# class ChapterForm(forms.Form):
#     your_name = forms.CharField(label="Your name", max_length=100)
class LoginForm(forms.Form):
    usernameLogin = forms.CharField(label="Username")    
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
