
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_projectmanagement_team'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
