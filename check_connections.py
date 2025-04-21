#!/usr/bin/env python
import os
import sys
import time
import django
from django.db import connections

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "research_admin.settings")
django.setup()

MAX_RETRIES = 10
RETRY_INTERVAL = 3  # segundos

print("==== Verificando conexiones a bases de datos ====")


def check_cvlac_connection():
    """Verificar conexión a CvLAC database"""
    from cvlac.models import Identificacion

    for attempt in range(MAX_RETRIES):
        try:
            count = Identificacion.objects.count()
            print(f"✅ Conexión a CvLAC exitosa - {count} investigadores encontrados")
            return True
        except Exception as e:
            print(f"❌ Intento {attempt+1}/{MAX_RETRIES} error conectando a CvLAC: {e}")
            if attempt < MAX_RETRIES - 1:
                print(f"⏱️ Esperando {RETRY_INTERVAL} segundos...")
                time.sleep(RETRY_INTERVAL)

    return False


def check_gruplac_connection():
    """Verificar conexión a GrupLAC database"""
    from gruplac.models import DatosBasicos

    for attempt in range(MAX_RETRIES):
        try:
            count = DatosBasicos.objects.count()
            print(f"✅ Conexión a GrupLAC exitosa - {count} grupos encontrados")
            return True
        except Exception as e:
            print(
                f"❌ Intento {attempt+1}/{MAX_RETRIES} error conectando a GrupLAC: {e}"
            )
            if attempt < MAX_RETRIES - 1:
                print(f"⏱️ Esperando {RETRY_INTERVAL} segundos...")
                time.sleep(RETRY_INTERVAL)

    return False


def check_integration_tables():
    """Verificar tablas de integración"""
    from integration.models import InvestigadorGrupo

    for attempt in range(MAX_RETRIES):
        try:
            try:
                count = InvestigadorGrupo.objects.count()
                print(
                    f"✅ Tablas de integración existentes - {count} relaciones encontradas"
                )
                return True
            except Exception as e:
                if "relation" in str(e) and "does not exist" in str(e):
                    print(
                        "⚠️ Las tablas de integración no existen - ejecutando migraciones"
                    )
                    from django.core.management import call_command

                    call_command("migrate")
                    print("✅ Migraciones aplicadas correctamente")
                    return True
                else:
                    raise e
        except Exception as e:
            print(
                f"❌ Intento {attempt+1}/{MAX_RETRIES} error accediendo a tablas de integración: {e}"
            )
            if attempt < MAX_RETRIES - 1:
                print(f"⏱️ Esperando {RETRY_INTERVAL} segundos...")
                time.sleep(RETRY_INTERVAL)

    return False


# Ejecutar verificaciones
cvlac_ok = check_cvlac_connection()
gruplac_ok = check_gruplac_connection()
integration_ok = check_integration_tables()

print("\n==== Resultado del diagnóstico ====")
print(f"CvLAC: {'✅ Conectado' if cvlac_ok else '❌ Falló la conexión'}")
print(f"GrupLAC: {'✅ Conectado' if gruplac_ok else '❌ Falló la conexión'}")
print(f"Tablas de integración: {'✅ OK' if integration_ok else '❌ Falló'}")

# Salir con código de error si alguna conexión falló
if not (cvlac_ok and gruplac_ok and integration_ok):
    print("\n❌ ERROR: No se pudieron establecer todas las conexiones necesarias.")
    sys.exit(1)
else:
    print("\n✅ ÉXITO: Todas las conexiones establecidas correctamente.")
    sys.exit(0)
