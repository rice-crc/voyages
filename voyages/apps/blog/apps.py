from django.apps import AppConfig





class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voyages.apps.blog'

        
    def ready(self):        
        import voyages.apps.blog.signals
        
