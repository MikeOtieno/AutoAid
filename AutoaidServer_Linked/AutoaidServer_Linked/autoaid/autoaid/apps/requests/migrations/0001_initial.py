
from django.db import migrations, models
import django.db.models.deletion
import uuid

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('garages', '0001_initial'),
        ('diagnostics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notes', models.TextField(blank=True)),
                ('preferred_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('CANCELLED', 'Cancelled'), ('COMPLETED', 'Completed')], default='PENDING', max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('garage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='garages.garage')),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='diagnostics.vehicleissue')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='users.user')),
            ],
        ),
    ]
