# Generated by Django 4.2 on 2023-05-21 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepost',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]