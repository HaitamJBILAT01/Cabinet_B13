from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    """
    Renders the login form and handles authentication.
    On success, redirects to LOGIN_REDIRECT_URL defined in settings.
    """
    template_name = 'comptes/login.html'
    redirect_authenticated_user = True
