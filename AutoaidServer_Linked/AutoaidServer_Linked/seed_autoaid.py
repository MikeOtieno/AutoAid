import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "autoaid"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autoaid.settings.development')
import django
django.setup()

from autoaid.apps.garages.models import Garage
from autoaid.apps.users.models import User

GARAGES = [
    dict(name='Nairobi Auto Care', address='Mombasa Road, Nairobi', phone='+254700111222', email='care@garage.example', latitude=-1.3192, longitude=36.8473, services=['Engine', 'Battery', 'Diagnostics'], rating=4.6),
    dict(name='Westlands Brake & Tyre Centre', address='Waiyaki Way, Westlands', phone='+254700222333', email='brake@garage.example', latitude=-1.2647, longitude=36.8029, services=['Brake', 'Tyres', 'Suspension'], rating=4.5),
    dict(name='Karen Garage Works', address='Karen Road, Nairobi', phone='+254700333444', email='karen@garage.example', latitude=-1.3197, longitude=36.7073, services=['Towing', 'Body Damage', 'Engine'], rating=4.3),
    dict(name='CBD Quick Mechanics', address='Moi Avenue, Nairobi CBD', phone='+254700444555', email='cbd@garage.example', latitude=-1.2864, longitude=36.8172, services=['Battery', 'Ignition', 'Electrical'], rating=4.4),
    dict(name='Thika Road Auto Clinic', address='Thika Road, Nairobi', phone='+254700555666', email='thika@garage.example', latitude=-1.2196, longitude=36.8861, services=['Engine', 'Oil Leak', 'Cooling System'], rating=4.2),
]

for g in GARAGES:
    Garage.objects.update_or_create(name=g['name'], defaults=g)

User.objects.filter(email='driver@test.com').delete()
User.objects.create_user(email='driver@test.com', password='password123', name='Test Driver', phone='0712345678')
print('Seed complete: created/updated 5 garages and test user driver@test.com / password123')
