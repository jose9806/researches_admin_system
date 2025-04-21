class DefaultRouter:
    """Router para modelos que van a la base de datos principal (scrap_db)"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label in ["integration", "gruplac", "core"]:
            return "default"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ["integration", "gruplac", "core"]:
            return "default"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        apps = ["integration", "gruplac", "core"]
        if obj1._meta.app_label in apps and obj2._meta.app_label in apps:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in ["integration", "core"]:
            return db == "default"
        elif app_label == "gruplac":
            # No permitir migraciones para gruplac (DB existente)
            return False
        return None


class CvlacRouter:
    """Router para la app CvLAC"""

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "cvlac":
            return "cvlac"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "cvlac":
            return "cvlac"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "cvlac" and obj2._meta.app_label == "cvlac":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "cvlac":
            return False  # No permitir migraciones para cvlac
        return None
