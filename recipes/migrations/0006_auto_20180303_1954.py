# Generated by Django 2.0.2 on 2018-03-03 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20180301_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientportion',
            name='subproduct',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portions', to='recipes.SubProduct'),
        ),
    ]
