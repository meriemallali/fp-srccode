
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_dmchat_chatgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmchat',
            name='chat_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
