from .forms import UserLoginForm,  UserPasswordChangeForm, UserRegisterForm

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.edit import CreateView

# - - - - - - - - - - - - - - - - - - - - CBV (Class Based View) - - - - - - - - - - - - - - - - - - - - #

class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'accounts/login-register.html' 

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context['login'] = True
        return context  

class UserLogoutView(LogoutView):
    pass

class UserPasswordChangeView(PasswordChangeView): # LoginRequiredMixin
    form_class = UserPasswordChangeForm 
    template_name = 'accounts/password-change.html' 

    def get_context_data(self, **kwargs):
        context = super(UserPasswordChangeView, self).get_context_data(**kwargs)
        if self.request.GET.get('changed') == 'true':
            context['changed'] = True
        return context

    def get_success_url(self, **kwargs):    
        return reverse('accounts:password-change') + '?changed=true' # hardcoded

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounts/login-register.html'

    def get_context_data(self, **kwargs):
        context = super(UserRegisterView, self).get_context_data(**kwargs)
        context['register'] = True
        return context

    def get_success_url(self, **kwargs):  
        return reverse('accounts:login')  
    
# - - - - - - - - - - - - - - - - - - - - FBV (Function Based View) - - - - - - - - - - - - - - - - - - - - #

def password_reset_view(request):
    return HttpResponse("?") # to implement
