import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_gestion_pacientes.settings')
django.setup()

from Gestion_Salud.models import HealthcareCenter

def populate():
    print("Iniciando población de Centros de Salud...")
    
    centers = [
        {
            "name": "Hospital Regional del Maule",
            "type": "Hospital",
            "is_public": True,
            "region": "Maule",
            "city": "Talca",
            "address": "Calle 1 Norte 123"
        },
        {
            "name": "CESFAM La Florida",
            "type": "CESFAM",
            "is_public": True,
            "region": "Maule",
            "city": "Talca",
            "address": "Calle Los Aromos 456"
        },
        {
            "name": "Hospital San Juan de Dios de Cauquenes",
            "type": "Hospital",
            "is_public": True,
            "region": "Maule",
            "city": "Cauquenes",
            "address": "Av. Doctor Meza 789"
        }
    ]

    for data in centers:
        # Usamos update_or_create para asegurar que los datos estén actualizados si ya existe
        obj, created = HealthcareCenter.objects.update_or_create(
            name=data['name'],
            defaults=data
        )
        
        action = "Creado" if created else "Actualizado"
        print(f"[{action}] {obj}")

    print("Proceso finalizado exitosamente.")

if __name__ == '__main__':
    populate()
