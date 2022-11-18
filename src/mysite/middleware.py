from django.urls import reverse
from django.http import HttpResponseRedirect

class AuthRequiredMiddleware:
    '''
    Redirect user to login page if not authenticated (from evrywhere \ {accounts, admin})  > it makes sense to keep it after including LoginRequiredMixin (?)
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            parent_path = request.path_info.strip().split('/')[1]   
            if parent_path not in ["accounts", "admin"]:
                return HttpResponseRedirect(reverse("accounts:login"))
        response = self.get_response(request)        
        return response