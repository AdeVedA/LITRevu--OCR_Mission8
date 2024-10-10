from django.contrib import admin
from .models import Ticket, Review, UserFollows, UserBlock
from .forms import TicketForm, ReviewForm, StarRatingWidget


class TicketAdmin(admin.ModelAdmin):
    form = TicketForm
    fieldsets = [
        ("Billet", {"fields": ["title", "description", "image"]}),
        ("Créateur", {"fields": ["user"]}),
    ]
    list_display = ["title", "user", "has_a_review", "description", "image", "time_created", "was_published_recently"]
    list_filter = ["time_created"]
    search_fields = ["title"]

class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm
    fieldsets = [
        ("Critique", {"fields": ["headline", "rating", "body"]}),
        ("Créateur", {"fields": ["user"]}),
        ("Billet lié (en réponse à...)", {"fields": ["ticket"]}),
    ]
    list_display = ["headline", "rating", "user", "time_created", "body", "ticket"]
    list_filter = ["time_created"]
    search_fields = ["headline"]
    
    # Surcharger la méthode formfield_for_dbfield pour utiliser 
    # l'élégant widget de formulaire en étoiles pour l'administration
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'rating':
            kwargs['widget'] = StarRatingWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)

class UserFollowsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Utilisateur", {"fields": ["user"]}),
        ("Utilisateurs suivis", {"fields": ["followed_user"]}),
    ]
    list_display = ["user", "followed_user"]

class UserBlockAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Utilisateur", {"fields": ["user"]}),
        ("Utilisateurs bloqués", {"fields": ["blocked_user"]}),
    ]
    list_display = ["user", "blocked_user"]

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
admin.site.register(UserBlock, UserBlockAdmin)