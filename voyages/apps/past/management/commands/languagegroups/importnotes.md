## first need to record what the language groups associated with the contributions were. 

the language groups were all changed by hand and so the data is going to have to be matched back up by hand. we're probably going to do this by name for the existing 50 contributions, but lat/long could come in handy.
	
	select * from
	(select id,language_group_id from past_enslavedcontributionlanguageentry) as cle join
	(select id, name, longitude,latitude from past_languagegroup) as lg on (cle.language_group_id=lg.id);


## then wipe out the necessary foreign keys

	update past_enslaved set language_group_id=Null;
	delete from past_moderncountry_languages;
	update past_enslavedcontributionlanguageentry set language_group_id=Null;
	delete from past_altlanguagegroupname;
	delete from past_languagegroup;


## the below fix two bad countries after the fact

	update past_moderncountry set name="Other" where id=9999;
	update past_moderncountry_languages set moderncountry_id=6021 where moderncountry_id=6087;
	
	


ascension island
mccarthy island
charlotte