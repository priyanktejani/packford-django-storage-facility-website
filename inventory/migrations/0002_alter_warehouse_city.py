# Generated by Django 4.0.1 on 2022-03-04 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='city',
            field=models.CharField(choices=[('London', 'London'), ('Sheffield', 'Sheffield'), ('Liverpool', 'Completed'), ('Bristol', 'Sussex'), ('Hertfordshire', 'Hertfordshire'), ('Birmingham', 'Glasgow'), ('Wales', 'Wales'), ('Kent', 'Kent'), ('Leicester', 'Leicester'), ('Coventry', 'Coventry')], max_length=20),
        ),
    ]
