# Generated by Django 2.1.4 on 2018-12-23 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_scrapedurls_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawlerurls',
            name='scraping',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scrapedurls',
            name='scraping',
            field=models.BooleanField(default=False),
        ),
    ]