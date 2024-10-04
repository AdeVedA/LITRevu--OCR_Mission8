from django.urls import path
from .views import FluxView, PostsView, SubscriptionView, TicketView, ReviewView, BilletReviewView, PostDeleteView


app_name = "blog"
urlpatterns = [
    # authentifié :
    path('flux/', FluxView.as_view(), name='flux'),
    path('mesposts/', PostsView.as_view(), name='mesposts'),
    path('mesabonnements/', SubscriptionView.as_view(), name='mesabonnements'),
    path('creer_billet/', TicketView.as_view(), name='creer_billet'),  # Page d'un billet
    path('creer_critique/<int:ticket_id>/', ReviewView.as_view(), name='creer_critique'),  # Page d'une critique
    path('creer_billet-critique/', BilletReviewView.as_view(), name='creer_billet-critique'),
    path('modifier_billet/<int:ticket_id>/', TicketView.as_view(), name='modifier_billet'),
    path('modifier_critique/<int:review_id>/', ReviewView.as_view(), name='modifier_critique'),
    path('supprimer/<str:post_type>/<int:post_id>/', PostDeleteView.as_view(), name='supprimer_post'),
]
