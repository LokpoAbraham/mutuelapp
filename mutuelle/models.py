from django.db import models
from django.conf import settings

# ---------- Section ----------
# Représente une section géographique ou de rattachement dans la mutuelle (ex: COCODY, YOPOUGON, etc.)
class Section(models.Model):
    nom = models.CharField(max_length=100)
    def __str__(self):
        return self.nom

# ---------- ParametreCotisation ----------
# Permet de paramétrer les taux de chaque type de cotisation (mensuelle, décès homme/femme, exceptionnelle, projet)
# Ajoute une date d’effet et un statut actif pour gérer les changements de montant dans le temps.
class ParametreCotisation(models.Model):
    TYPE_CHOICES = [
        ('Mensuelle', 'Mensuelle'),
        ('Deces_H', 'Décès Homme'),
        ('Deces_F', 'Décès Femme'),
        ('Exceptionnelle', 'Exceptionnelle'),
        ('Projet', 'Projet')
    ]
    type_cotisation = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_effet = models.DateField()
    actif = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.get_type_cotisation_display()} - {self.montant} à partir du {self.date_effet}"

# ---------- Adherent ----------
# Représente chaque membre de la mutuelle, avec toutes ses infos personnelles, sa section, son état (actif, suspendu, décédé)
class Adherent(models.Model):
    SEXE_CHOICES = [('H', 'Homme'), ('F', 'Femme')]
    ETAT_CHOICES = [('Actif', 'Actif'), ('Suspendu', 'Suspendu'), ('Décédé', 'Décédé')]
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=100)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    telephone1 = models.CharField(max_length=20)
    telephone2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_adhesion = models.DateField()
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES)
    fonction = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.nom} {self.prenoms}"

# ---------- Deces ----------
# Représente un décès déclaré (lié à un adhérent), permet de centraliser tous les événements de décès pour la gestion des cotisations décès
class Deces(models.Model):
    adherent_defunt = models.ForeignKey(Adherent, on_delete=models.SET_NULL, null=True, related_name='deces')
    date_deces = models.DateField()
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    observations = models.CharField(max_length=200, blank=True, null=True)
    exercice = models.ForeignKey('Exercice', on_delete=models.PROTECT, related_name='deces_enregistres', null=True, blank=True)
    def __str__(self):
        return f"{self.adherent_defunt} ({self.date_deces})"

# ---------- CotisationMensuelle ----------
# Stocke chaque paiement de cotisation mensuelle par adhérent, pour un mois/année donné, avec la section de rattachement.
class CotisationMensuelle(models.Model):
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    mois = models.CharField(max_length=20)
    annee = models.IntegerField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    exercice = models.ForeignKey('Exercice', on_delete=models.PROTECT, related_name='cotisations_mensuelles', null=True, blank=True)
    def __str__(self):
        return f"{self.adherent} - {self.mois}/{self.annee}"

# ---------- CotisationDeces ----------
# Garde la trace des cotisations décès versées pour chaque décès déclaré, pour chaque adhérent.
class CotisationDeces(models.Model):
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE, related_name='cotisations_deces')
    deces = models.ForeignKey(Deces, on_delete=models.CASCADE, related_name='cotisations')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    sexe = models.CharField(max_length=1, choices=[('H', 'Homme'), ('F', 'Femme')])
    exercice = models.ForeignKey('Exercice', on_delete=models.PROTECT, related_name='cotisations_deces', null=True, blank=True)
    def __str__(self):
        return f"{self.adherent} - {self.deces}"

# ---------- CotisationExceptionnelle ----------
# Garde la trace des cotisations exceptionnelles (pour projets spécifiques, urgences, etc.), reliées à chaque adhérent et section.
class CotisationExceptionnelle(models.Model):
    libelle = models.CharField(max_length=200) # nom ou motif de la cotisation (projet, don, urgence)
    date_debut = models.DateField()
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    projet = models.CharField(max_length=200, blank=True, null=True) # nom du projet, si besoin
    exercice = models.ForeignKey('Exercice', on_delete=models.PROTECT, related_name='cotisations_exceptionnelles')
    def __str__(self):
        return f"{self.libelle} - {self.adherent}"

# ---------- Depense ----------
# Permet de saisir toutes les dépenses de la mutuelle (fonctionnement, décès, projets), avec une typologie claire pour les bilans.
class Depense(models.Model):
    TYPE_CHOICES = [
        ('Fonctionnement', 'Fonctionnement'),
        ('Décès', 'Décès'),
        ('Projet', 'Projet/Exceptionnelle')
    ]
    date = models.DateField()
    libelle = models.CharField(max_length=200) # motif ou intitulé de la dépense
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_depense = models.CharField(max_length=30, choices=TYPE_CHOICES)
    observation = models.CharField(max_length=200, blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    exercice = models.ForeignKey('Exercice', on_delete=models.PROTECT, related_name='depenses')  # AJOUTE
    def __str__(self):
        return f"{self.type_depense} - {self.libelle} ({self.date})"


# ---------- Profile ----------
# Permet de lier un utilisateur Django à un profil spécifique de la mutuelle, avec une section de rattachement.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.section}"
    
    # models.py

class Exercice(models.Model):
    nom = models.CharField(max_length=100, unique=True, help_text="Nom de l'exercice (ex : 2023)")
    date_debut = models.DateField()
    date_fin = models.DateField()
    cloture = models.BooleanField(default=False, help_text="L’exercice est-il clôturé ?")

    def __str__(self):
        return self.nom