# Generated by Django 3.1.1 on 2020-09-26 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'катгория', 'verbose_name_plural': 'катгории'},
        ),
    ]
