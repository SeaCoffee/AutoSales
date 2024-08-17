# Generated by Django 5.1 on 2024-08-14 17:16

import core.enums.country_region_enum
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cars', '0001_initial'),
        ('currency', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ListingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('listing_photo', models.ImageField(blank=True, null=True, upload_to='upload_photo_listing', validators=[django.core.validators.FileExtensionValidator(['jpeg', 'jpg', 'png'])])),
                ('active', models.BooleanField(default=False)),
                ('views_day', models.IntegerField(default=0)),
                ('views_week', models.IntegerField(default=0)),
                ('views_month', models.IntegerField(default=0)),
                ('edit_attempts', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_usd', models.DecimalField(decimal_places=2, editable=False, max_digits=10, null=True)),
                ('price_eur', models.DecimalField(decimal_places=2, editable=False, max_digits=10, null=True)),
                ('price_uah', models.DecimalField(decimal_places=2, editable=False, max_digits=10, null=True)),
                ('region', models.CharField(choices=core.enums.country_region_enum.Region.choices, default=core.enums.country_region_enum.Region['KYIV'], max_length=50)),
                ('year', models.IntegerField()),
                ('engine', models.CharField(max_length=255)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='cars.carmodel')),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings', to='currency.currencymodel')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'listings',
            },
        ),
    ]
