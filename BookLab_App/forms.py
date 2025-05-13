from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import Contact

class contectForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')


class SingupForm(UserCreationForm):
   email =  forms.EmailField(required=True)

   class Meta:
      model = User
      fields=  ['username','email','password1','password2']

   def _init_(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class LoginForm(forms.Form):
   username  = forms.CharField(max_length=150)
   password   = forms.CharField(widget=forms.PasswordInput())




class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is not registered.")
        return email
