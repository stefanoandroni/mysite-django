from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm 
from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_attrs = {
                'class': 'form-control',
            }
            self.fields[field].widget.attrs.update(new_attrs) 

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_attrs = {
                'class': 'form-control',
            }
            self.fields[field].widget.attrs.update(new_attrs) 
            
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_attrs = {
                'class': 'form-control',
            }
            self.fields[field].widget.attrs.update(new_attrs) 
    



