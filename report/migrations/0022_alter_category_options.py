# Generated by Django 4.2 on 2023-05-21 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0021_alter_category_options_alter_alimony_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Bölüm', 'verbose_name_plural': 'Bölümler'},
        ),
    ]