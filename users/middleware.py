from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout

class BanCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.is_banned:
            logout(request)
            messages.error(request, "🚫 Your account has been banned.")
            return redirect('login')
