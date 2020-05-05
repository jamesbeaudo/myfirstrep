# Generated by Django 2.2.6 on 2020-01-30 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('users', '0003_auto_20200129_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamcreation',
            name='author',
        ),
        migrations.RemoveField(
            model_name='teamcreation',
            name='date_posted',
        ),
        migrations.RemoveField(
            model_name='teamcreation',
            name='team_key',
        ),
        migrations.RemoveField(
            model_name='teamcreation',
            name='team_name',
        ),
        migrations.AddField(
            model_name='teamcreation',
            name='email_alias',
            field=models.EmailField(blank=True, default='', max_length=70),
        ),
        migrations.AddField(
            model_name='teamcreation',
            name='group',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]