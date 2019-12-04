# Generated by Django 2.2.1 on 2019-05-29 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20190529_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='join',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='myapp.Destination'),
        ),
        migrations.AlterField(
            model_name='join',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='myapp.User'),
        ),
    ]