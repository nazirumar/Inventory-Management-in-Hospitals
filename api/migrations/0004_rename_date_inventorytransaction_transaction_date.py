# Generated by Django 5.1.2 on 2024-10-30 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_inventoryitem_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventorytransaction',
            old_name='date',
            new_name='transaction_date',
        ),
    ]
