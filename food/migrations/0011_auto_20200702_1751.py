# Generated by Django 3.0.7 on 2020-07-02 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20200702_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientparent',
            name='created',
        ),
        migrations.RemoveField(
            model_name='ingredientparent',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='ingredientquality',
            name='created',
        ),
        migrations.RemoveField(
            model_name='ingredientquality',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='ingredienttype',
            name='created',
        ),
        migrations.RemoveField(
            model_name='ingredienttype',
            name='updated',
        ),
        migrations.AlterField(
            model_name='calorie',
            name='food',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='calorie', serialize=False, to='food.Food'),
        ),
        migrations.AlterField(
            model_name='drymatter',
            name='food',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='drymatter', serialize=False, to='food.Food'),
        ),
        migrations.AlterField(
            model_name='guaranteed',
            name='food',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='guaranteed', serialize=False, to='food.Food'),
        ),
    ]
