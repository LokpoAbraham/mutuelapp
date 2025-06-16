from django import forms
from mutuelle.models import Adherent, Section
from datetime import date
from mutuelle.models import CotisationMensuelle
from mutuelle.models import CotisationDeces, CotisationExceptionnelle
from mutuelle.models import Depense
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from mutuelle.models import Profile
from mutuelle.models import Exercice
from .models import ParametreCotisation


MOIS_CHOICES = [
    ('Janvier', 'Janvier'), ('Février', 'Février'), ('Mars', 'Mars'), ('Avril', 'Avril'),
    ('Mai', 'Mai'), ('Juin', 'Juin'), ('Juillet', 'Juillet'), ('Août', 'Août'),
    ('Septembre', 'Septembre'), ('Octobre', 'Octobre'), ('Novembre', 'Novembre'), ('Décembre', 'Décembre'),
]

class CotMensuelleMultiMoisForm(forms.Form):
    adherent = forms.ModelChoiceField(queryset=Adherent.objects.all(), label="Adhérent")
    annee = forms.IntegerField(initial=date.today().year, label="Année")
    mois = forms.MultipleChoiceField(choices=MOIS_CHOICES, widget=forms.CheckboxSelectMultiple, label="Mois à payer")
    montant = forms.DecimalField(label="Montant (fixé)", disabled=True)
    date_paiement = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), label="Date paiement")
    exercice = forms.ModelChoiceField(queryset=None, label="Exercice")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from mutuelle.models import Exercice
        self.fields['exercice'].queryset = Exercice.objects.filter(cloture=False)

class CotMensuelleForm(forms.ModelForm):
    class Meta:
        model = CotisationMensuelle
        fields = ['adherent', 'mois', 'annee', 'montant', 'date_paiement', 'section', 'exercice']

class CotDecesForm(forms.ModelForm):
    class Meta:
        model = CotisationDeces
        fields = ['adherent', 'deces', 'montant', 'date_paiement', 'section', 'sexe', 'exercice']

class CotExceptionnelleForm(forms.ModelForm):
    class Meta:
        model = CotisationExceptionnelle
        fields = ['libelle', 'date_debut', 'adherent', 'montant', 'section', 'projet', 'exercice']

class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['date', 'libelle', 'montant', 'type_depense', 'observation', 'section', 'exercice']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }



User = get_user_model()

class AssignRoleForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Utilisateur")
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Rôle (groupe)")
    section = forms.ModelChoiceField(queryset=Section.objects.all(), required=False, label="Section (si applicable)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionnel : Tu peux filtrer les utilisateurs par “non superuser”
        self.fields['user'].queryset = User.objects.filter(is_superuser=False)

class AssignRoleForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.order_by('username'), label="Utilisateur")
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Rôle (groupe)")
    section = forms.ModelChoiceField(queryset=Section.objects.all(), required=False, label="Section (si applicable)")



class ExerciceForm(forms.ModelForm):
    class Meta:
        model = Exercice
        fields = ['nom', 'date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': True}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Exercice 2025', 'required': True}),
        }


class ParametreCotisationForm(forms.ModelForm):
    class Meta:
        model = ParametreCotisation
        fields = ['montant', 'actif', 'date_effet']  # On retire 'type_cotisation'
        widgets = {
            'date_effet': forms.DateInput(attrs={'type': 'date'}),
        }
