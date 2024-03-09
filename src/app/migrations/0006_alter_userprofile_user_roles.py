
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_userprofile_user_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_roles',
            field=models.CharField(choices=[('admin', 'Admin'), ('project manager', 'Project Manager'), ('lead', 'Lead')], max_length=50, null=True),
        ),
    ]
