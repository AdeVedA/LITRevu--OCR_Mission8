import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib import admin


class UserFollows(models.Model):
# classe pour le suivi d'utilisateurs
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')  # Utilisateur qui suit
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')  # Utilisateur suivi

    class Meta:
        # s'assurer de ne pas avoir plusieurs instances de UserFollows
        # et de n'avoir que des paires uniques user-user_followed
        unique_together = ('user', 'followed_user', )
        verbose_name = 'réseau social'
        verbose_name_plural = 'Utilisateurs & Suivis'

    def __str__(self):
        return f'{self.user} suit {self.followed_user}'

class UserBlock(models.Model):
# classe pour le blocage d'utilisateurs

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocking')  # Utilisateur qui bloque
    blocked_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocked_by')  # Utilisateur bloqué

    class Meta:
        # s'assurer de ne pas avoir plusieurs instances de UserBlock
        # et n'avoir que des paires uniques user-blocked_user
        unique_together = ('user', 'blocked_user', )

    def __str__(self):
        return f'{self.user} a bloqué {self.blocked_user}'

class Ticket(models.Model):
# Modèle Ticket pour une demande de critique

    title = models.CharField(max_length=128, verbose_name="Titre")  # Titre du livre ou article
    description = models.TextField(max_length=1024, verbose_name="Description", blank=True)  # Description ou résumé de la demande de critique
    time_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création") # Date de création/publication
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # L'utilisateur qui a créé le billet
    image = models.ImageField(null=True, blank=True, verbose_name="image du billet", default='no_image.png') # image du billet

    IMAGE_MAX_FILE_SIZE = 2 * 1024 * 1024  # Limite de taille : 2 MB
    
    @admin.display(
        boolean=True,
        ordering="time_created",
        description="published recently?"
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=3) <= self.time_created <= now
    
    def has_a_review(self):
        return self.review_set.exists()
    
    @staticmethod
    def valid_image_size(image):
        if image.size > Ticket.IMAGE_MAX_FILE_SIZE:
            return False, "La taille de l'image dépasse la limite autorisée de 2 MB."
        return True, None
    
    class Meta:
        verbose_name = 'Billet'
        verbose_name_plural = 'Tous les billets'
        ordering = ['-time_created']

    def __str__(self):
        return f"{self.title} créé par {self.user}"

class Review(models.Model):
# Modèle Review pour une critique de livre/article

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # valide que l'évaluation soit bien entre 0 et 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Critique'
        verbose_name_plural = 'Toutes les critiques'
        ordering = ['time_created']

    def __str__(self):
        return f"{self.headline} par {self.user}"
