import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_gestion_pacientes.settings')
django.setup()

from Gestion_Salud.models import User, HealthcareCenter

def populate_data():
    print("=== Iniciando Población de Datos ===")

    # 1. Crear Centros de Salud
    print("\n[1/2] Creando Centros de Salud...")
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
        obj, created = HealthcareCenter.objects.update_or_create(
            name=data['name'],
            defaults=data
        )
        action = "Creado" if created else "Actualizado"
        print(f"   -> {action}: {obj}")

    # 2. Crear Usuarios
    print("\n[2/2] Creando Usuarios de Prueba...")
    users_data = [
        {
            "username": "administrativo",
            "password": "password123",
            "first_name": "Juan",
            "last_name": "Pérez",
            "rut": "12.345.678-5",
            "email": "juan.perez@hospital.cl",
            "institutional_email": "juan.perez@hospital.cl",
            "position": "ADMINISTRATIVO",
            "birth_date": "1980-01-01"
        },
        {
            "username": "medico",
            "password": "password123",
            "first_name": "Gregory",
            "last_name": "House",
            "rut": "26.583.190-7",
            "email": "gregory.house@hospital.cl",
            "institutional_email": "gregory.house@hospital.cl",
            "position": "MEDICO",
            "birth_date": "1975-05-15"
        },
        {
            "username": "enfermera",
            "password": "password123",
            "first_name": "Carla",
            "last_name": "Espinosa",
            "rut": "11.111.111-1",
            "email": "carla.espinosa@hospital.cl",
            "institutional_email": "carla.espinosa@hospital.cl",
            "position": "ENFERMERA",
            "birth_date": "1985-03-20"
        }
    ]

    for data in users_data:
        rut = data.pop("rut")
        password = data.pop("password")
        
        user, created = User.objects.update_or_create(
            rut=rut,
            defaults=data
        )
        
        if created:
            user.set_password(password)
            user.save()
            print(f"   -> Creado: {user.username} ({data['position']})")
        else:
            user.set_password(password)
            user.save()
            print(f"   -> Actualizado: {user.username} ({data['position']})")

    print("\n=== Población Finalizada Exitosamente ===")

if __name__ == '__main__':
    populate_data()
