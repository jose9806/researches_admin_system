import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "research_admin.settings")
django.setup()

from django.db import connections
from cvlac.models import Identificacion
from gruplac.models import DatosBasicos
from integration.models import InvestigadorGrupo

print("==== Verificando conexiones a bases de datos ====")

# Verificar conexión a CvLAC
try:
    count = Identificacion.objects.count()
    print(f"✅ Conexión a CvLAC exitosa - {count} investigadores encontrados")
except Exception as e:
    print(f"❌ Error conectando a CvLAC: {e}")

# Verificar conexión a GrupLAC (scrap_db)
try:
    count = DatosBasicos.objects.count()
    print(f"✅ Conexión a GrupLAC exitosa - {count} grupos encontrados")
except Exception as e:
    print(f"❌ Error conectando a GrupLAC: {e}")

# Verificar tablas de integración
try:
    # Intentar crear las tablas si no existen
    from django.db import connection

    cursor = connection.cursor()
    try:
        count = InvestigadorGrupo.objects.count()
        print(f"✅ Tablas de integración existentes - {count} relaciones encontradas")
    except Exception as e:
        if "relation" in str(e) and "does not exist" in str(e):
            print("⚠️ Las tablas de integración no existen - ejecuta migraciones")
        else:
            print(f"❌ Error accediendo a tablas de integración: {e}")
except Exception as e:
    print(f"❌ Error general: {e}")

print("\n==== Diagnóstico completo ====")
