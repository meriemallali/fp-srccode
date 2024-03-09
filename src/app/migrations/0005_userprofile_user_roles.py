
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_team_members_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_roles',
            field=models.CharField(choices=[('admin', 'Admin'), ('project manager', 'Project Manager')], max_length=50, null=True),
        ),
    ]
