from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout, get_user_model

from .forms import SignUpForm


User = get_user_model()

# dans authentication/views.py :

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    def get(self, request):
        return render(request, 'authentication/login.html')
    def get_success_url(self):
        return '/flux/'  # Redirige l'utilisateur authentifié vers la page d'accueil

# gestion de l'inscription des utilisateurs
class SignUpView(FormView):
    template_name = 'authentication/signup.html'
    form_class = SignUpForm
    success_url = '/flux/'  # Rediriger vers la page d'accueil après l'inscription

    def form_valid(self, form):
        # Sauvegarde/crée l'utilisateur en base de données
        form.save()
        # Récupère le nom d'utilisateur et le mot de passe "brut" (non hashé)
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        # Authentifie l'utilisateur avec son nom d'utilisateur et son mot de passe
        user = authenticate(username=username, password=raw_password)
        # Connecte l'utilisateur à la session (si l'authentification réussit)
        login(self.request, user)
        # Continue le flux normal en appelant la méthode form_valid() de la classe parente
        return super().form_valid(form)

# déconnexion des utilisateurs
class CustomLogoutView(View):
    # Méthode qui s'exécute lorsqu'une requête GET est envoyée à cette vue
    def get(self, request):
        # Déconnecte l'utilisateur actuel
        logout(request)
        return render(request, 'authentication/logout.html')
    # définir une page vers laquelle rediriger après déconnexion (timer dans html)
    next_page = ''