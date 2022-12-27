# Generated by Django 3.2.7 on 2021-10-01 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_alter_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asknewpassword',
            name='user',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]