from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('coredata', '0021_fix_table_names'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='committee',
            table='coredata_committee',
        ),
        migrations.AlterModelTable(
            name='jobtitle',
            table='coredata_jobtitle',
        ),
        migrations.AlterModelTable(
            name='student',
            table='coredata_student',
        ),
    ]