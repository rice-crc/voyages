
drop references from individuals to the language groups

	update past_enslaved set language_group_id=Null;

then drop all references between language groups and modern countries

	delete from past_moderncountry_languages;

these next two can't be reversed because they're links to the old language names!!

	delete from past_moderncountry_languages;
	delete from past_enslavedcontributionlanguageentry;
	delete from past_altlanguagegroupname;

finally let's drop the languages table

	delete from past_languagegroup;
	

now let's add the languages back in

	python3.6 manage.py updatelanguagegroups