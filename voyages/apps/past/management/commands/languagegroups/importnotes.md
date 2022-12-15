update past_enslaved set language_group_id=Null;
delete from past_moderncountry_languages;
delete from past_moderncountry_languages;
delete from past_enslavedcontributionlanguageentry;
delete from past_altlanguagegroupname;
delete from past_languagegroup;




from voyages.apps.past.models import *
mcs=ModernCountry.objects.all()
mc=mcs.get(pk=9999)
mc.delete()
mc=mcs.get(pk=6087) 
mc.delete()