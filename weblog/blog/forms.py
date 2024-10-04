from django import forms
from .models import Review, Ticket


class FollowUserForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': "Nom d'utilisateur",
            'class': 'form-control'
        }),
        label=''
    )

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'maxlength': '150', 'class': 'text-center'}),
            'description': forms.Textarea(attrs={'maxlength': '1440', 'rows': '5'}),
            'image': forms.ClearableFileInput(),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Appel de la méthode statique valid_image_size 
            # pour vérifier la taille du fichier de l'image
            is_valid, size_error_message = Ticket.valid_image_size(image)
            if not is_valid:
                raise forms.ValidationError(size_error_message)
        return image

class StarRatingWidget(forms.Select):
    def __init__(self, attrs=None):
        super().__init__(attrs, choices=[(i, '★' * i + '☆' * (5-i)) for i in range(6)])

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'rating': forms.RadioSelect(choices=[(0, ' - 0'), (1, ' - 1'), (2, ' - 2'), (3, ' - 3'), (4, ' - 4'), (5, ' - 5')]),
            'body': forms.Textarea(attrs={'rows': '5'})
        }
