from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Champ requis. Saisissez une adresse email valide.',
        error_messages={
            'unique': "Cette adresse e-mail est déjà utilisée. N'êtes-vous pas déjà inscrit ?",
            'invalid': 'Saisissez une adresse email valide.',
        }
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Supprimer les messages d'aide par défaut
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        
        # Définir les labels personnalisés
        self.fields['username'].label = 'Votre Nom d\'utilisateur'
        self.fields['email'].label = 'Votre adresse e-mail'
        self.fields['password1'].label = 'Votre mot de passe'
        self.fields['password2'].label = 'Confirmez votre mot de passe'

        # Définir les placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Nom d\'utilisateur'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Mot de passe'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmer le mot de passe'

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Cette adresse e-mail est déjà utilisée. N'êtes-vous pas déjà inscrit ?")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        # Utilisation des validateurs de mot de passe de Django
        validate_password(password1)
        return password1

    # Validation de la correspondance des mots de passe
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        
        return password2
