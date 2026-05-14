
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Garage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=32)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('services', models.JSONField(blank=True, default=list)),
                ('rating', models.FloatField(default=4.5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
