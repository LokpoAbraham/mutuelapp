# Generated by Django 5.2.2 on 2025-06-15 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mutuelle', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExerciceArchive',
        ),
        migrations.AddField(
            model_name='cotisationdeces',
            name='exercice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cotisations_deces', to='mutuelle.exercice'),
        ),
        migrations.AddField(
            model_name='cotisationmensuelle',
            name='exercice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cotisations_mensuelles', to='mutuelle.exercice'),
        ),
        migrations.AddField(
            model_name='deces',
            name='exercice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='deces_enregistres', to='mutuelle.exercice'),
        ),
        migrations.AlterField(
            model_name='cotisationexceptionnelle',
            name='exercice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cotisations_exceptionnelles', to='mutuelle.exercice'),
        ),
    ]
