# Generated by Django 2.1.4 on 2018-12-21 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20181221_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapedurls',
            name='relatedUrl',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ScrapedUrls', verbose_name='Related Url'),
        ),
    ]
