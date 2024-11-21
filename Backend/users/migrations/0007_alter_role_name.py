# Generated by Django 5.1.3 on 2024-11-21 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_role_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('supervisor', 'Super Visor'), ('manager', 'Manager'), ('employee', 'Employee'), ('rep', 'Reporter'), ('customer', 'Customer'), ('credit_card_holder', 'Credit Cardholder'), ('supervisor_employee', 'Supervisor')], default='employee', max_length=100, unique=True),
        ),
    ]
