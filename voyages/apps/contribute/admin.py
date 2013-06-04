from django.contrib import admin

# Hide the Site and Group features
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
admin.site.unregister(Site)
admin.site.unregister(Group)