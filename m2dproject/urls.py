from django.contrib import admin
from django.urls import path
from mutuelle import views
from django.contrib.auth import views as auth_views
from mutuelle.views import assign_role
from mutuelle.views import parametres_cotisation_list
from mutuelle.views import export_cotisations_pdf
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),                # Pour accéder à l'admin Django
    path('dashboard/', views.dashboard, name='dashboard'),  # Pour ton dashboard
    path('adherents/', views.adherents_list, name='adherents_list'), # Pour la liste des adhérents
    path('adherents/ajouter/', views.adherent_create, name='adherent_create'), # Pour ajouter un adhérent
    path('adherents/modifier/<int:pk>/', views.adherent_update, name='adherent_update'), # Pour modifier un adhérent
    path('adherents/suspendre/<int:pk>/', views.adherent_suspend, name='adherent_suspend'),# Pour suspendre un adhérent
    path('adherents/deces/<int:pk>/', views.adherent_deces, name='adherent_deces'),# Pour marquer un adhérent comme décédé
    path('adherents/detail/<int:pk>/', views.adherent_detail, name='adherent_detail'),# Pour voir les détails d'un adhérent
    path('cotisations/', views.cotisations_list, name='cotisations_list'),# Pour la liste des cotisations
    path('cotisations/ajouter/', views.cotisation_create, name='cotisation_create'),# Pour ajouter une cotisation
    path('cotisations/ajouter-multi/', views.cotisation_mensuelle_multimois, name='cotisation_mensuelle_multimois'),
    path('cotisations/modifier/<str:type>/<int:pk>/', views.cotisation_update, name='cotisation_update'),
    path('cotisations/supprimer/<str:type>/<int:pk>/', views.cotisation_delete, name='cotisation_delete'),
    path('depenses/', views.depenses_list, name='depenses_list'),
    path('depenses/ajouter/', views.depense_create, name='depense_create'),
    path('depenses/modifier/<int:pk>/', views.depense_update, name='depense_update'),
    path('depenses/supprimer/<int:pk>/', views.depense_delete, name='depense_delete'),
    path('bilan/', views.bilan_global, name='bilan_global'),
    path('bilan/export_excel/', views.bilan_export_excel, name='bilan_export_excel'),
    path('bilan/drilldown/', views.bilan_drilldown, name='bilan_drilldown'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('assign-role/', assign_role, name='assign_role'),
    path('exercice/<int:pk>/cloturer/', views.cloturer_exercice, name='cloturer_exercice'),
    path('exercice/<int:pk>/decloturer/', views.decloturer_exercice, name='decloturer_exercice'),
    path('exercices/', views.exercices_list, name='exercices_list'),
    path('exercices/ajouter/', views.exercice_create, name='exercice_create'),
    path('profil/', views.profile_view, name='profile'),
    path('mot-de-passe/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='change_password'),
    path('mot-de-passe/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('parametres-cotisation/', parametres_cotisation_list, name='parametres_cotisation_list'),
    path('parametres-cotisation/<int:pk>/edit/', views.parametre_edit, name='parametre_edit'),
    path('parametres-cotisation/<int:pk>/toggle/', views.parametre_toggle_actif, name='parametre_toggle_actif'),
    path('export/membres/', views.export_membres_excel, name='export_membres_excel'),
    path('export/membres/pdf/', views.export_membres_pdf, name='export_membres_pdf'),
    path('export/cotisations/', views.export_cotisations_excel, name='export_cotisations_excel'),
    path("import/adherents/", views.import_adherents, name="import_adherents"),
    path("import/cotisations/", views.import_cotisations, name="import_cotisations"),
    path("import/depenses/", views.import_depenses, name="import_depenses"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),  # ou une vue simple
    path("ajout-utilisateur/", views.ajout_utilisateur, name="ajout_utilisateur"),

# Ajoute ici d'autres routes si besoin
]

urlpatterns += [
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('export/cotisations/pdf/', export_cotisations_pdf, name='export_cotisations_pdf'),
]

