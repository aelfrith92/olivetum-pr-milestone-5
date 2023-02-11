# Generated by Django 3.2 on 2023-02-02 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0003_product_has_child_variants'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('title', models.TextField(max_length=255)),
                ('body', models.TextField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('single_rating', models.IntegerField(choices=[(1, '1'),
                                                               (2, '2'),
                                                               (3, '3'),
                                                               (4, '4'),
                                                               (5, '5')])),
                ('verified_purchase', models.BooleanField(default=False)),
                ('product',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='reviews',
                                   to='products.product')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('business_name', models.CharField(max_length=255)),
                ('risk_lev',
                 models.IntegerField(choices=[(1, 'Simplified_DD'),
                                              (2, 'Standard_DD'),
                                              (3, 'Enhanced_DD')])),
                ('city', models.CharField(max_length=255)),
                ('location',
                 location_field.models.plain.PlainLocationField(max_length=63)
                 ),
                ('ship_abroad', models.BooleanField(default=False)),
                ('slr_rating',
                 models.IntegerField(choices=[(1, '1'),
                                              (2, '2'),
                                              (3, '3'),
                                              (4, '4'),
                                              (5, '5')])),
                ('point_of_contact',
                 models.ForeignKey(null=True,
                                   on_delete=django.db.models.deletion.SET_NULL,
                                   related_name='users',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-slr_rating'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id',
                 models.BigAutoField(auto_created=True,
                                     primary_key=True,
                                     serialize=False,
                                     verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('body', models.TextField(max_length=255)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('product',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='comments',
                                   to='products.product')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
