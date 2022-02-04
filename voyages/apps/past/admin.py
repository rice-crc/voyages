from django.contrib import admin

from voyages.apps.voyage.forms import extract

from .models import LanguageGroup, AltLanguageGroupName, ModernCountry, RegisterCountry, CaptiveFate, CaptiveStatus

class NamedModelFormAbstractBase(admin.ModelAdmin):
    search_fields = ['id', 'name']

    class Meta:
        fields = '__all__'

class AltLanguageGroupNameInline(admin.TabularInline):
    model = AltLanguageGroupName
    extra = 0

class LanguageGroupForm(NamedModelFormAbstractBase):
    inlines = (AltLanguageGroupNameInline,)

admin.site.register(LanguageGroup, LanguageGroupForm)
admin.site.register(ModernCountry, NamedModelFormAbstractBase)
admin.site.register(RegisterCountry, NamedModelFormAbstractBase)
admin.site.register(CaptiveFate, NamedModelFormAbstractBase)
admin.site.register(CaptiveStatus, NamedModelFormAbstractBase)