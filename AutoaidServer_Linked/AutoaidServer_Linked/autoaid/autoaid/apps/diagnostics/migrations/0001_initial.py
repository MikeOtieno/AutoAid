
from django.db import migrations, models
import django.db.models.deletion
import uuid

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleIssue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('problem_text', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('RECEIVED', 'Received'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='RECEIVED', max_length=16)),
                ('callback_url', models.URLField(blank=True)),
                ('callback_delivered_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='UploadedMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('media_type', models.CharField(choices=[('IMAGE', 'Image'), ('AUDIO', 'Audio')], max_length=8)),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('original_name', models.CharField(blank=True, max_length=512)),
                ('content_type', models.CharField(blank=True, max_length=128)),
                ('size_bytes', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='diagnostics.vehicleissue')),
            ],
        ),
        migrations.CreateModel(
            name='DiagnosisResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('diagnosis', models.CharField(max_length=255)),
                ('confidence', models.FloatField()),
                ('recommended_action', models.CharField(max_length=255)),
                ('possible_causes', models.JSONField(default=list)),
                ('requires_mechanic', models.BooleanField(default=False)),
                ('explanation', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('issue', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='diagnosis', to='diagnostics.vehicleissue')),
            ],
        ),
    ]
