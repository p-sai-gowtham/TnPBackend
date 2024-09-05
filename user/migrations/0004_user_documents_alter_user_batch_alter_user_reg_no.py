# Generated by Django 5.1 on 2024-08-18 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        ('user', '0003_user_drives'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='documents',
            field=models.ManyToManyField(related_name='users', to='home.document'),
        ),
        migrations.AlterField(
            model_name='user',
            name='batch',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='reg_no',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]