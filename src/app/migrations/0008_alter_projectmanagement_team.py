
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_teamproject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmanagement',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='app.teamproject'),
        ),
    ]
