# Generated by Django 4.2.1 on 2023-05-29 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_profile_photo_alter_project_photos'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='discussion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.discussion'),
        ),
    ]
