
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('NOT STARTED', 'Not started '), ('IN PROGRESS', 'In Progress'), ('DONE', 'Done')], default='NOT STARTED', max_length=20),
        ),
    ]
