from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args,**kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist!')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password!')
            if not user.is_active:
                raise forms.ValidationError('This user is not active!')
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput,label='Confirm Password')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords do not match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email address is already taken")
        return email
