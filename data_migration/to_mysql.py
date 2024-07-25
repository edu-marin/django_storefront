import pandas as pd
import os
import django
import sys

# Asegúrate de que la raíz del proyecto esté en el path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')

# Configura Django
django.setup()

from store.models import Customer

# Supongamos que tienes un DataFrame con los datos
data = {
    'first_name': ['John', 'Jane'],
    'last_name': ['Doe', 'Doe'],
    'email': ['john.doe@example.com', 'jane.doe@example.com'],
    'phone': ['123456789', '987654321'],
    'address': ['123 Main St', '456 Elm St']
}

df = pd.DataFrame(data)

for index, row in df.iterrows():
    Customer.objects.create(
        first_name=row['first_name'],
        last_name=row['last_name'],
        email=row['email'],
        phone=row['phone'],
        address=row['address']
    )

print("Database populated successfully!")
