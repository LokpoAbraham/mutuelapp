from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('mutuelle', '0003_add_exercice_to_cotisationexceptionnelle'),  # ou la dernière migration chez toi
    ]

    operations = [
        migrations.AddField(
            model_name='depense',
            name='exercice',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='depenses', to='mutuelle.exercice'),
        ),
    ]
