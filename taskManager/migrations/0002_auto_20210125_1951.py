# Generated by Django 2.2.4 on 2021-01-25 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskManager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='task',
            name='categories',
            field=models.ManyToManyField(related_name='tasksAssociated', to='taskManager.Category'),
        ),
        migrations.AddField(
            model_name='task',
            name='isCompleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasksOwned', to='taskManager.User'),
        ),
    ]
