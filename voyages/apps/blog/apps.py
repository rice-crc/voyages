from django.apps import AppConfig

import logging



#logging.getLogger('blog').info("apps.py")

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voyages.apps.blog'

    logging.info("BlogConfig class")
        
    def ready(self):
        logging.info("ready")
        import voyages.apps.blog.signals
        logging.info("ready apos")

        #return super().ready()
        
