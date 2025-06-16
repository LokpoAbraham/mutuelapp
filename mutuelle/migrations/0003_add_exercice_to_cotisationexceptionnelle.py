from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('mutuelle', '0002_delete_exercicearchive_cotisationdeces_exercice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotisationexceptionnelle',
            name='exercice',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='cotisations_exceptionnelles', to='mutuelle.exercice'),
        ),
    ]
