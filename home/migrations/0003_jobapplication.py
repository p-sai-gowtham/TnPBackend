# Generated by Django 5.0.1 on 2024-08-24 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_document_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('job_description', models.TextField()),
                ('application_deadline', models.DateField()),
                ('drive_date', models.DateField()),
                ('job_application_link', models.URLField()),
            ],
        ),
    ]
