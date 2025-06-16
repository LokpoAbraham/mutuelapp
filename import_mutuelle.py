import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'm2dproject.settings')
django.setup()

from mutuelle.models import (
    Section, Adherent, CotisationMensuelle, CotisationDeces,
    CotisationExceptionnelle, Depense
)
from django.utils.dateparse import parse_date

# === 1. Import des Adhérents ===
df_adh = pd.read_excel('Adherents_modele.xlsx')
for _, row in df_adh.iterrows():
    section, _ = Section.objects.get_or_create(nom=row['section'])
    adherent, created = Adherent.objects.get_or_create(
        nom=row['nom'],
        prenoms=row['prenoms'],
        defaults={
            'sexe': row['sexe (H/F)'],
            'section': section,
            'telephone1': row.get('telephone1', ''),
            'telephone2': row.get('telephone2', ''),
            'email': row.get('email', ''),
            'etat': row.get('etat (Actif/Suspendu/Décédé)', 'Actif'),
            'date_adhesion': parse_date(str(row.get('date_adhesion (YYYY-MM-DD)', None))),
            'fonction': row.get('fonction', ''),
        }
    )
    if created:
        print(f"[Adhérent] {row['nom']} {row['prenoms']} ajouté")
    else:
        print(f"[Adhérent] {row['nom']} {row['prenoms']} déjà existant, non réimporté")

# === 2. Import des Cotisations Mensuelles ===
df_mens = pd.read_excel('CotisationsMensuelles_modele.xlsx')
for _, row in df_mens.iterrows():
    try:
        adherent = Adherent.objects.get(nom=row['nom'], prenoms=row['prenoms'])
        section = Section.objects.get(nom=row['section'])
        cot, created = CotisationMensuelle.objects.get_or_create(
            adherent=adherent,
            mois=str(row['mois (01-12 ou janvier-décembre)']),
            annee=int(row['annee (YYYY)']),
            defaults={
                'montant': row['montant'],
                'date_paiement': parse_date(str(row.get('date_paiement (YYYY-MM-DD)', None))),
                'section': section
            }
        )
        if created:
            print(f"[Mensuelle] {adherent} - {row['mois (01-12 ou janvier-décembre)']}/{row['annee (YYYY)']} ajouté")
    except Exception as e:
        print(f"Erreur cotisation mensuelle : {row['nom']} {row['prenoms']} - {e}")

# === 3. Import des Cotisations Décès ===
df_deces = pd.read_excel('CotisationsDeces_modele.xlsx')
for _, row in df_deces.iterrows():
    try:
        adherent = Adherent.objects.get(nom=row['nom'], prenoms=row['prenoms'])
        section = Section.objects.get(nom=row['section'])
        cot, created = CotisationDeces.objects.get_or_create(
            adherent=adherent,
            beneficiaire=row['beneficiaire'],
            defaults={
                'montant': row['montant'],
                'date_paiement': parse_date(str(row.get('date_paiement (YYYY-MM-DD)', None))),
                'section': section,
                'sexe': adherent.sexe
            }
        )
        if created:
            print(f"[Décès] {adherent} > {row['beneficiaire']} ajouté")
    except Exception as e:
        print(f"Erreur cotisation décès : {row['nom']} {row['prenoms']} - {e}")

# === 4. Import des Cotisations Exceptionnelles ===
df_exc = pd.read_excel('CotisationsExceptionnelles_modele.xlsx')
for _, row in df_exc.iterrows():
    try:
        adherent = Adherent.objects.get(nom=row['nom'], prenoms=row['prenoms'])
        section = Section.objects.get(nom=row['section'])
        cot, created = CotisationExceptionnelle.objects.get_or_create(
            adherent=adherent,
            libelle=row['libelle (motif de la cotisation)'],
            montant=row['montant'],
            date_debut=parse_date(str(row.get('date_paiement (YYYY-MM-DD)', None))),
            section=section
        )
        if created:
            print(f"[Exceptionnelle] {adherent} - {row['libelle (motif de la cotisation)']} ajouté")
    except Exception as e:
        print(f"Erreur cotisation exceptionnelle : {row['nom']} {row['prenoms']} - {e}")

# === 5. Import des Dépenses ===
df_dep = pd.read_excel('Depenses_modele.xlsx')
for _, row in df_dep.iterrows():
    try:
        section = Section.objects.get(nom=row['section'])
        dep, created = Depense.objects.get_or_create(
            libelle=row['libelle (motif de la dépense)'],
            date=parse_date(str(row['date (YYYY-MM-DD)'])),
            type_depense=row['type_depense (Fonctionnement/Décès/Projet)'],
            montant=row['montant'],
            observation=row.get('observation', ''),
            section=section
        )
        if created:
            print(f"[Dépense] {row['libelle (motif de la dépense)']} - {row['date (YYYY-MM-DD)']} ajouté")
    except Exception as e:
        print(f"Erreur dépense : {row['libelle (motif de la dépense)']} - {e}")

print("=== IMPORTATION TERMINÉE ===")