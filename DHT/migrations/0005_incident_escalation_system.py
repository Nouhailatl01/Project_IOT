# Generated migration for escalation system

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DHT', '0004_incident_is_product_lost_operateur_email_and_more'),
    ]

    operations = [
        # Supprimer les anciens champs
        migrations.RemoveField(
            model_name='incident',
            name='op1_ack',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='op2_ack',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='op3_ack',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='op1_saved_at',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='op2_saved_at',
        ),
        migrations.RemoveField(
            model_name='incident',
            name='op3_saved_at',
        ),
        
        # Ajouter les nouveaux champs
        migrations.AddField(
            model_name='incident',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='incident',
            name='current_escalation_level',
            field=models.IntegerField(
                choices=[(1, 'Opérateur 1'), (2, 'Opérateur 2'), (3, 'Opérateur 3')],
                default=1
            ),
        ),
        migrations.AddField(
            model_name='incident',
            name='escalation_counter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='incident',
            name='escalated_to_op2_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='incident',
            name='escalated_to_op3_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='incident',
            name='op1_responded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='incident',
            name='op2_responded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='incident',
            name='op3_responded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='incident',
            name='op1_responded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='incident',
            name='op2_responded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='incident',
            name='op3_responded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
