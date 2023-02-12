# Generated by Django 3.2 on 2023-02-06 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20230206_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='provider',
            field=models.ForeignKey(blank=True,
                                    null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    to='products.provider'),
        ),
        migrations.AlterField(
            model_name='provider',
            name='point_of_contact',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]