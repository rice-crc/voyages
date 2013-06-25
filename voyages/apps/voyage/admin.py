from django.contrib import admin
from django.contrib.admin.widgets import *
from django.contrib.flatpages.models import FlatPage
from django.forms import *
from django.utils.translation import ugettext as _
from .models import *

class FlatPageAdmin(admin.ModelAdmin):
    """
    Support for flat page.
    """
    fields = ('url', 'title', 'content')
    readonly_fields = ('url', 'title',)
    
    list_display = ['title', 'url']
  
    # prevents deleting of flat page
    actions = None

    # Prevents anyone from trying to add a new flat page
    def has_add_permission(self, request):
        return False

    class Media:
        js = ( 'scripts/tiny_mce/tinymce.min.js',
              'scripts/tiny_mce/textareas.js',
              )


class VoyageAdminForm(ModelForm):
    mm = ModelMultipleChoiceField(
        queryset=VoyageCaptain.objects.all(),
        widget=FilteredSelectMultiple(_('Captains'), False, attrs={'rows':'10'}))

    def __init__(self, *args, **kwargs):

        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['mm'] = [t.service.pk for t in kwargs['instance'].message_forum_set.all()]

        BaseModelForm.__init__(self, *args, **kwargs)
        #forms.ModelForm.__init__(self, *args, **kwargss)

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, commit)

        old_save_m2m = self.save_m2m
        def save_m2m():
            old_save_m2m()

            messages = [s for s in self.cleaned_data['ss']]
            for mf in instance.message_forum_set.all():
                if mf.service not in messages:
                    mf.delete()
                else:
                    messages.remove(mf.service)

            for capt in Captain:
                VoyageCaptain.objects.create(name=capt, forum=instance)

        self.save_m2m = save_m2m

        return instance

    class Meta:
        model = Voyage

class VoyageAdmin(admin.ModelAdmin):
    form = VoyageAdminForm

# We have to unregister it, and then reregister
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Voyage, VoyageAdmin)
admin.site.register(VoyageGroupings)
admin.site.register(VoyageShip)
admin.site.register(VoyageOutcome)
admin.site.register(VoyageItinerary)
admin.site.register(VoyageDates)
admin.site.register(VoyageCaptain)
admin.site.register(VoyageCrew)
admin.site.register(VoyageSlavesCharacteristics)
admin.site.register(VoyageSources)
admin.site.register(Region)
admin.site.register(BroadRegion)
admin.site.register(Place)