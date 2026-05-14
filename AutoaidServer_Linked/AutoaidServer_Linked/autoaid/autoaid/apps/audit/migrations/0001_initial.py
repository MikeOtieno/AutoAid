
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
            name='AuditEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('action', models.CharField(max_length=64)),
                ('object_type', models.CharField(blank=True, max_length=64)),
                ('object_id', models.CharField(blank=True, max_length=64)),
                ('ip_address', models.CharField(blank=True, max_length=64)),
                ('user_agent', models.CharField(blank=True, max_length=256)),
                ('request_id', models.CharField(blank=True, max_length=64)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
            ],
            options={
                'indexes': [models.Index(fields=['action', 'created_at'], name='audit_action_created_idx'), models.Index(fields=['user', 'created_at'], name='audit_user_created_idx')],
            }
        ),
    ]
