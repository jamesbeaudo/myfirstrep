# Generated by Django 2.2.6 on 2020-02-11 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_auto_20200211_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='team_num1',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
