
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0009_delete_member_delete_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttasks',
            name='assigned_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_by_task', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projecttasks',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to_task', to=settings.AUTH_USER_MODEL),
        ),
    ]
