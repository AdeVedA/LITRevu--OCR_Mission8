from django.views import View
from django.urls import reverse, reverse_lazy # reverse_lazy permet de rediriger vers une URL une fois une action terminée
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from .forms import FollowUserForm, TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows, UserBlock


User = get_user_model()

class FluxView(LoginRequiredMixin, View):
    # Cette vue nécessite que l'utilisateur soit connecté (LoginRequiredMixin)

    def get(self, request):
        # Récupérer l'utilisateur connecté
        user = request.user
        # Récupérer les utilisateurs que cet utilisateur suit
        followed_users = UserFollows.objects.filter(user=user).values_list('followed_user', flat=True)

        # Récupérer les tickets créés par l'utilisateur ou par ceux qu'il suit
        tickets = Ticket.objects.filter(user__in=[user] + list(followed_users)).order_by('-time_created')
        for ticket in tickets: # Ajouter un attribut type pour les identifier dans le html
            ticket.type = 'ticket'

        # Récupérer les critiques associées à ces tickets
        reviews = Review.objects.filter(ticket__in=tickets).order_by('-time_created')
        reviewed_ticket_ids = {review.ticket.id for review in reviews}  # Set des IDs de tickets avec critiques
        for review in reviews: # Ajouter attribut d'identification
            review.type = 'review'
            review.star_rating = '★' * review.rating + '☆' * (5 - review.rating)

        # Filtrer les tickets pour exclure ceux qui ont déjà une critique
        tickets_without_reviews = [ticket for ticket in tickets if ticket.id not in reviewed_ticket_ids]

        # Combiner les deux et les trier par ordre de création (antéchronologique)
        flux_items = sorted(list(tickets_without_reviews) + list(reviews), key=lambda x: x.time_created, reverse=True)

        # Préparer le contexte avec la liste des éléments du flux
        context = {
            'flux_items': flux_items,  # Liste des tickets
        }

        # Rendre le template 'flux.html' avec le contexte
        return render(request, 'blog/flux.html', context)

class PostsView(LoginRequiredMixin, TemplateView):
    # Cette vue nécessite que l'utilisateur soit connecté (LoginRequiredMixin)
    template_name = 'blog/mesposts.html'
    
    def get(self, request):
        # Récupérer l'utilisateur connecté
        user = request.user

        # Récupérer les tickets créés par l'utilisateur
        tickets = Ticket.objects.filter(user=user)
        for ticket in tickets: 
            # Ajouter un attribut type pour les identifier dans le html
            ticket.type = 'ticket'

        # Récupérer les critiques créées par l'utilisateur
        reviews = Review.objects.filter(user=user)
        for review in reviews: 
            # Ajouter attribut d'identification
            review.type = 'review'
            review.star_rating = '★' * review.rating + '☆' * (5 - review.rating)

        # Set des IDs de tickets avec critiques
        # reviewed_ticket_ids = {review.ticket.id for review in reviews}
        # Filtrer les tickets pour exclure ceux qui ont déjà une critique
        # tickets_without_reviews = [ticket for ticket in tickets if ticket.id not in reviewed_ticket_ids]

        # Combiner les deux et les trier par ordre de création (antéchronologique)
        mesposts_items = sorted(list(tickets) + list(reviews), key=lambda x: x.time_created, reverse=True)

        # Préparer le contexte avec la liste des éléments du flux
        context = {
            'mesposts_items': mesposts_items,
            # Liste des posts de l'utilisateur
        }
        return render(request,'blog/mesposts.html', context)

class SubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/mesabonnements.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # le formulaire pour suivre d'autres utilisateurs
        context['form'] = FollowUserForm()
        # les abonnements actuels de l'utilisateur
        context['user_follows'] = UserFollows.objects.filter(user=self.request.user)
        # les abonnés (ceux qui suivent l'utilisateur)
        context['followers'] = UserFollows.objects.filter(followed_user=self.request.user)
        # les utilisateurs bloqués par l'utilisateur connecté
        context['blocked_users'] = UserBlock.objects.filter(user=self.request.user).select_related('blocked_user')
        return context

    def post(self, request, *args, **kwargs):
        # Méthode qui gère les requêtes HTTP POST
        # pour suivre un utilisateur
        if 'follow' in request.POST:
            form = FollowUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                try:
                    user_to_follow = User.objects.get(username=username)
                    user_already_followed = UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists()
                    user_blocked_you = UserBlock.objects.filter(user=user_to_follow, blocked_user=request.user).exists()
                    
                    # si utilisateur bloqué par l'utilisateur qu'il veut suivre
                    if user_blocked_you:
                        messages.error(request, f"{username} vous a bloqué. Vous ne pouvez pas le suivre.")
                    # si utilisateur déjà suiveur de l'utilisateur qu'il veut suivre
                    elif user_already_followed:
                        messages.error(request, f"Vous suivez déjà {username}.")
                    # sinon on inscrit le nouveau suivi demandé
                    else:
                        UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
                        messages.success(request, f"Vous suivez maintenant {username}.")
                # et si jamais l'utilisateur n'existe pas...
                except User.DoesNotExist:
                    messages.error(request, f"Aucun utilisateur trouvé avec le nom {username}.")

        # pour se désabonner d'un utilisateur
        elif 'unfollow' in request.POST:
            user_id = request.POST.get('unfollow_user_id')
            try:
                user_to_unfollow = User.objects.get(id=user_id)
                UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow).delete()
                messages.success(request, f"Vous avez arrêté de suivre {user_to_unfollow.username}.")
            except User.DoesNotExist:
                messages.error(request, f"Utilisateur non trouvé.")

        # pour bloquer un utilisateur qui nous suit
        elif 'block' in request.POST:
            user_id = request.POST.get('block_user_id')
            try:
                user_to_block = get_object_or_404(User, id=user_id)
            
                # Supprimer l'abonnement (le suivi)
                UserFollows.objects.filter(user=user_to_block, followed_user=request.user).delete()
                # Créer une relation de blocage
                UserBlock.objects.get_or_create(user=request.user, blocked_user=user_to_block)
                # Message notifiant le blocage
                messages.success(request, f"Vous avez bloqué {user_to_block.username}.")
            except User.DoesNotExist:
                messages.error(request, f"Utilisateur non trouvé.")

        elif 'unblock' in request.POST:
            # Déblocage d'un utilisateur
            user_id = request.POST.get('unblock_user_id')
            try:
                user_to_unblock = get_object_or_404(User, id=user_id)
                
                # Supprimer la relation de blocage
                UserBlock.objects.filter(user=request.user, blocked_user=user_to_unblock).delete()
                messages.success(request, f"Vous avez débloqué {user_to_unblock.username}.")
            except User.DoesNotExist:
                messages.error(request, f"Utilisateur non trouvé.")

        return redirect(reverse('blog:mesabonnements'))

# Vue pour la création ou la modification d'un billet
class TicketView(LoginRequiredMixin, CreateView, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'blog/modifier_billet.html'
    success_url = reverse_lazy('blog:mesposts') # Redirection vers le flux après modification ou création

    # Méthode pour afficher le formulaire
    def get_object(self):
        # Récupérer le ticket s'il y a un `ticket_id` dans les kwargs, sinon renvoyer None
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            return get_object_or_404(Ticket, id=ticket_id)
        return None

    def form_valid(self, form):
        # Associer l'utilisateur connecté au billet
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs.get('ticket_id')
        if ticket_id:
            context['is_editing'] = True # Pour différencier création / modification dans le template
        return context

# Vue pour la création d'une critique en réponse à un billet
class ReviewView(LoginRequiredMixin, CreateView, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'blog/creer_critique.html'

    def get_object(self, queryset=None):
        """
        Si un ID de critique est présent dans l'URL, on récupère l'objet Review correspondant.
        Sinon, on retourne None, ce qui signifie qu'on crée une nouvelle critique.
        """
        review_id = self.kwargs.get('review_id')  # On récupère l'ID de la critique
        if review_id:
            return get_object_or_404(Review, id=review_id)
        return None

    # Surcharge de la méthode de récupération de contexte pour inclure le billet dans le contexte
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.get_object():
            # En modification, on récupère le ticket lié à la critique
            ticket = self.get_object().ticket
        else:
            # En création, on récupère le ticket via l'ID de l'URL
            ticket_id = self.kwargs['ticket_id']
            ticket = get_object_or_404(Ticket, id=ticket_id)
        
        # Ajouter le ticket au contexte pour l'afficher dans le template
        context['ticket'] = ticket
        # Ajoute une variable pour indiquer si c'est une modification
        context['is_editing'] = True if self.get_object() else False
        return context

    # Surcharge pour associer la critique avec le billet et l'utilisateur
    def form_valid(self, form):
        if not self.get_object():  # Création : on associe le billet
            form.instance.ticket = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])

        form.instance.user = self.request.user  # L'utilisateur connecté devient l'auteur de la critique
        return super().form_valid(form)

    # Redirection après la création ou la modification de la critique
    def get_success_url(self):
        if not self.get_object():
            return reverse('blog:flux')  # Redirige vers le flux après l'envoi de la critique
        return reverse('blog:mesposts')  # Redirige vers le mesposts après la modification de la critique

class PostDeleteView(LoginRequiredMixin, View):

    def get_object(self, post_type, post_id):
        # Récupérer dynamiquement l'objet selon le type
        if post_type == 'ticket':
            return get_object_or_404(Ticket, id=post_id, user=self.request.user)
        elif post_type == 'review':
            return get_object_or_404(Review, id=post_id, user=self.request.user)
        else:
            # Si le type est invalide, retourne une 404
            raise Http404("Type de post invalide.")

    def post(self, request, post_type, post_id):
        # Récupérer l'objet à supprimer
        post = self.get_object(post_type, post_id)
        
        # Si l'utilisateur n'est pas le propriétaire du post, on le redirige sans supprimer
        if post.user != request.user:
            return redirect('blog:mesposts')

        # Supprimer lee post
        post.delete()

        # Rediriger après suppression
        return redirect('blog:mesposts')

class BilletReviewView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/creer_billet-critique.html'
    success_url = reverse_lazy('blog:flux')

    # Utilisation de form_class pour spécifier plusieurs formulaires
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket_form'] = TicketForm()
        context['review_form'] = ReviewForm()
        return context

    # Méthode pour gérer la soumission des deux formulaires
    def post(self, request, *args, **kwargs):
        ticket_form = TicketForm(self.request.POST, self.request.FILES)
        review_form = ReviewForm(self.request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            # Sauvegarde du billet
            ticket = ticket_form.save(commit=False)
            ticket.user = self.request.user  # Associer l'utilisateur connecté au billet
            ticket.save()

            # Sauvegarde de la critique
            review = review_form.save(commit=False)
            review.user = self.request.user  # Associer l'utilisateur connecté à la critique
            review.ticket = ticket  # Associer la critique au billet nouvellement créé
            review.save()

            # Rediriger vers une URL de succès après soumission
            return redirect(self.success_url)
        else:
            # Renvoyer le formulaire avec des erreurs
            return self.render_to_response(self.get_context_data(
                ticket_form=ticket_form, review_form=review_form
            ))


