import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_gestion_pacientes.settings')
django.setup()

from Gestion_Salud.models import User

def create_users():
    print("Creando usuarios de prueba...")

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
        
        # Usamos RUT como identificador único para evitar duplicados
        user, created = User.objects.update_or_create(
            rut=rut,
            defaults=data
        )
        
        if created:
            user.set_password(password)
            user.save()
            print(f"[CREADO] Usuario: {user.username} | Pass: {password} | Rol: {data['position']}")
        else:
            # Si ya existe, actualizamos password por si acaso
            user.set_password(password)
            user.save()
            print(f"[ACTUALIZADO] Usuario: {user.username} | Pass: {password} | Rol: {data['position']}")

    # Crear superusuario si no existe
    superuser_rut = "99.999.999-K"
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@hospital.cl",
            password="password123",
            rut=superuser_rut,
            institutional_email="admin@hospital.cl",
            position="ADMINISTRATIVO"
        )
        print(f"[CREADO] Superusuario: admin | Pass: password123")
    else:
        print("[INFO] Ya existe un superusuario.")

if __name__ == '__main__':
    create_users()
