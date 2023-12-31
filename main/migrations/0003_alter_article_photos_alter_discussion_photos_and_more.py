# Generated by Django 4.2.1 on 2023-05-22 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_article_options_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='photos',
            field=models.ImageField(blank=True, null=True, upload_to='media/img/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='photos',
            field=models.ImageField(blank=True, null=True, upload_to='media/img/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='photos',
            field=models.ImageField(blank=True, null=True, upload_to='media/img/%Y/%m/%d/'),
        ),
    ]
