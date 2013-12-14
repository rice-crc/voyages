#from voyages.apps.voyage.models import LegacyModel
import voyages
#from django.db import Model

class LegacyRouter(object):
    """
    Router to route legacy database operations to the correct database
    """
    def db_for_read(self, model, **hints):
        if issubclass(model, voyages.apps.voyage.legacy_models.LegacyModel):
            return 'legacy'
        return None
    def db_for_write(self, model, **hints):
        if issubclass(model, voyages.apps.voyage.legacy_models.LegacyModel):
            return False
        return None
    def allow_migrate(self, db, model):
        if db == 'legacy':
            return False
        elif issubclass(model, voyages.apps.voyage.legacy_models.LegacyModel):
            return False
        return None

