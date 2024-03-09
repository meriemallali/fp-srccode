
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_projecttasks_assigned_by_projecttasks_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_roles',
            field=models.CharField(blank=True, choices=[('admin', 'Admin'), ('project manager', 'Project Manager'), ('lead', 'Lead')], max_length=50, null=True),
        ),
    ]
