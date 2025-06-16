from django.contrib import admin
from .models import (
    Section, ParametreCotisation, Adherent, Deces,
    CotisationMensuelle, CotisationDeces, CotisationExceptionnelle,
    Depense, Profile, Exercice
)


# ========================== BASE FILTRAGE PAR SECTION ==========================
GROUPS_ALL_ACCESS = ['president', 'tresoriergeneral', 'secretairegeneral']

def user_has_section(user):
    return hasattr(user, 'profile') and user.profile.section

def get_section(user):
    if user_has_section(user):
        return user.profile.section
    return None

def section_filter_admin(qs, request):
    # Si admin général, accès total, sinon filtrage par section
    if request.user.is_superuser or request.user.groups.filter(name__in=GROUPS_ALL_ACCESS).exists():
        return qs
    section = get_section(request.user)
    if section:
        return qs.filter(section=section)
    return qs.none()

def section_foreignkey_admin(db_field, request, kwargs):
    if db_field.name == "section" and user_has_section(request.user):
        kwargs["queryset"] = Section.objects.filter(pk=request.user.profile.section.pk)
    return kwargs

def save_section_admin(request, obj):
    if not request.user.is_superuser and user_has_section(request.user):
        obj.section = request.user.profile.section

# ========================== SECTION ==========================
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom']
    search_fields = ['nom']

# ========================== ADHERENT ==========================
@admin.register(Adherent)
class AdherentAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenoms', 'sexe', 'section', 'etat', 'date_adhesion', 'fonction']
    list_filter = ['section', 'etat', 'sexe']
    search_fields = ['nom', 'prenoms', 'email', 'telephone1', 'telephone2']

    def get_queryset(self, request):
        return section_filter_admin(super().get_queryset(request), request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs = section_foreignkey_admin(db_field, request, kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        save_section_admin(request, obj)
        super().save_model(request, obj, form, change)

# ========================== PARAMETRE COTISATION ==========================
@admin.register(ParametreCotisation)
class ParametreCotisationAdmin(admin.ModelAdmin):
    list_display = ['type_cotisation', 'montant', 'date_effet', 'actif']
    list_filter = ['type_cotisation', 'actif']
    search_fields = ['type_cotisation']

# ========================== DECES ==========================
@admin.register(Deces)
class DecesAdmin(admin.ModelAdmin):
    list_display = ['adherent_defunt', 'date_deces', 'section', 'observations']
    list_filter = ['section', 'date_deces']
    search_fields = ['adherent_defunt__nom', 'adherent_defunt__prenoms']

    def get_queryset(self, request):
        return section_filter_admin(super().get_queryset(request), request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs = section_foreignkey_admin(db_field, request, kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        save_section_admin(request, obj)
        super().save_model(request, obj, form, change)

# ========================== COTISATION MENSUELLE ==========================
@admin.register(CotisationMensuelle)
class CotisationMensuelleAdmin(admin.ModelAdmin):
    list_display = ['adherent', 'mois', 'annee', 'montant', 'date_paiement', 'section']
    list_filter = ['annee', 'mois', 'section']
    search_fields = ['adherent__nom', 'adherent__prenoms']

    def get_queryset(self, request):
        return section_filter_admin(super().get_queryset(request), request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs = section_foreignkey_admin(db_field, request, kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        save_section_admin(request, obj)
        super().save_model(request, obj, form, change)

# ========================== COTISATION DECES ==========================
@admin.register(CotisationDeces)
class CotisationDecesAdmin(admin.ModelAdmin):
    list_display = ['adherent', 'deces', 'montant', 'date_paiement', 'section', 'sexe']
    list_filter = ['section', 'sexe']
    search_fields = ['adherent__nom', 'adherent__prenoms', 'deces__adherent_defunt__nom']

    def get_queryset(self, request):
        return section_filter_admin(super().get_queryset(request), request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs = section_foreignkey_admin(db_field, request, kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        save_section_admin(request, obj)
        super().save_model(request, obj, form, change)

# ========================== COTISATION EXCEPTIONNELLE ==========================
@admin.register(CotisationExceptionnelle)
class CotisationExceptionnelleAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'adherent', 'date_debut', 'montant', 'section', 'projet']
    list_filter = ['section', 'projet']
    search_fields = ['libelle', 'adherent__nom', 'adherent__prenoms']

    def get_queryset(self, request):
        return section_filter_admin(super().get_queryset(request), request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs = section_foreignkey_admin(db_field, request, kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        save_section_admin(request, obj)
        super().save_model(request, obj, form, change)

# ========================== DEPENSE ==========================
@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ['libelle', 'date', 'type_depense', 'montant', 'section', 'observation']
    list_filter = ['type_depense', 'section']
    search_fields = ['libelle', 'observation']

    def get_queryset(self, request):
        return section_filter_admin(super().get_queryset(request), request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs = section_foreignkey_admin(db_field, request, kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        save_section_admin(request, obj)
        super().save_model(request, obj, form, change)

# ========================== PROFILE ==========================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'section']
    search_fields = ['user__username', 'section__nom']


# ========================== EXERCICE ==========================
@admin.register(Exercice)
class ExerciceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_debut', 'date_fin', 'cloture')
    list_filter = ('cloture',)
    search_fields = ('nom',)
