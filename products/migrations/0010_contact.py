# Generated by Django 3.2 on 2023-02-10 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_provider_slr_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('query', models.TextField()),
                ('auth', models.BooleanField(default=False)),
            ],
        ),
    ]