# Generated by Django 3.2 on 2022-07-20 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamentos', '0004_remove_horario_cod'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horario',
            name='cliente',
        ),
        migrations.AddField(
            model_name='horario',
            name='cliente',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='usuario_agendou', to='agendamentos.Usuario'),
        ),
    ]