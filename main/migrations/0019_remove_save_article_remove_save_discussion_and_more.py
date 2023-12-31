# Generated by Django 4.2.1 on 2023-06-05 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('main', '0018_remove_like_article_remove_like_project_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='save',
            name='article',
        ),
        migrations.RemoveField(
            model_name='save',
            name='discussion',
        ),
        migrations.RemoveField(
            model_name='save',
            name='project',
        ),
        migrations.RemoveField(
            model_name='save',
            name='question',
        ),
        migrations.AddField(
            model_name='save',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='save',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
