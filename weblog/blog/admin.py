from django.contrib import admin
from .models import Ticket, Review, UserFollows, UserBlock
from .forms import TicketForm, ReviewForm


class TicketAdmin(admin.ModelAdmin):
    form = TicketForm
    fieldsets = [
        ("Billet", {"fields": ["title", "description", "image"]}),
        ("Créateur", {"fields": ["user"]}),
    ]
    # inlines =[DetailsInline]
    list_display = ["title", "time_created", "was_published_recently", "has_a_review", "description"]
    list_filter = ["time_created"]
    search_fields = ["title"]

class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm
    fieldsets = [
        ("Critique", {"fields": ["headline", "rating", "body"]}),
        ("Créateur", {"fields": ["user"]}),
        ("Billet lié (en réponse à...)", {"fields": ["ticket"]}),
    ]
    # inlines =[DetailsInline]
    list_display = ["headline", "rating", "time_created", "ticket", "user", "body"]
    list_filter = ["time_created"]
    search_fields = ["ticket"]

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