from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView, CustomLoginView, CustomLogoutView


app_name = "authentication"
urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
