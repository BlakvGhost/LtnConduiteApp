# Generated by Django 3.2.7 on 2021-10-01 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20211001_0008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='classe_niv',
        ),
    ]