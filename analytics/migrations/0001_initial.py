# Generated by Django 5.1.6 on 2025-02-16 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticsReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(max_length=100)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='reports/')),
            ],
        ),
    ]
