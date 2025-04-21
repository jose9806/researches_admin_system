class CvlacRouter:
    """
    Router for CvLAC app models.
    """
    app_label = 'cvlac'
    
    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'cvlac'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return 'cvlac'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == self.app_label and obj2._meta.app_label == self.app_label:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label:
            # Don't allow migrations for this app as we're using an existing database
            return False
        return None