from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('coredata', '0020_delete_filepermission'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='staff',
            table='coredata_staff',
        ),
        migrations.AlterModelTable(
            name='operationalplanitems',
            table='coredata_operationalplanitems',
        ),
    ]