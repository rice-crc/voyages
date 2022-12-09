# remaining work on maps ui

~~## 1. fix oddities with the search ui~~

~~* there are certain ports that aren't rendering properly when we search~~
~~	* rio pongo when region of embarkation is senegambia & offshore atlantic --> why is it even appearing in the results?~~

~~I am pretty sure this is an issue with the search ui, not with my use of it~~

## 2. handle mapping for geographically distributed languages

need stable m2m relations added to the language_group --> moderncountry

~~* waiting on philip & david for these~~
* waiting on domingos for proper integration of language_group into the search bar

~~## 3. handle mapping for overlapping nodes~~

~~* some language groups & even ports have the exact same lat/long, out to 7 decimal places~~
~~* I could make marker clustering to differentiate these (and may have to for #2 above...) but I think at base this is a data problem. if we're mapping with that kind of precision, then why do 5-ish Yoruba language groups have the exact same location?~~

## 4. translation

* need to integrate the terms used in the map into the django po's

## 5. more interactivity?

* zoom to fit
	* click on a region, it zooms you in to the bounds of the constituent ports
	* downside of this is that i'm not sure how the mobile would look
	* right now mouseover or click nodes gets you a popup -- adding click=zoom interactivity, would tablet users be unable to see those region popups because they'd be hurried into the port-level zoom?
* auto-filter origins
	* we're now showing routes to origins only when the connected nodes are moused over
	* but i could see it cleaning the interface up even further if that mouseover event hid the non-relevant origin nodes?
	* downside is that i'm not sure what subsequent user event would trigger the reappearance of those hidden nodes... we're getting close to functionality that is better handled as a query/search

## 6. manual data changes

* ports
	* 60699 to 7.9840736,4.5504317
	* 60502 to ???
	* 60917 to ???
	* 60220 to ???
	* 60501 looks to be way too far inland
	* 60264 to -13.2857840,8.4275610
	* something wrong with Iles Plantain -- route origin doesn't align with port location
* language_groups
	* 160219 to -8.0391000,5.1441000
	* 360605 to ???











Sierra Leone self-loops are messed up...

lg's
160272
160268
160499
160499
160515
160270
460675
111111
160279
160210
160269
160219
160218
160225
160274
160226
160277
160281
160155
160276
160208
160437
160282
160306
160511
460681
160280
160223
160271
160275
160325

itineraries
160272-60200-60200-60200
160268-60200-60200-60200
160499-60200-60200-60100
160499-60200-60200-35300
160515-60200-60200-60200
160270-60200-60200-60200
460675-60200-60200-60200
111111-60200-60200-60100
None-60200-60200-35300
160279-60200-60200-60200
160210-60200-60200-60200
160269-60200-60200-60200
160219-60200-60200-60200
None-60200-60200-60100
160218-60200-60200-60200
160225-60200-60200-60200
160274-60200-60200-60200
160226-60200-60200-60200
160277-60200-60200-60200
160281-60200-60200-60200
160155-60200-60200-60200
160276-60200-60200-60200
160208-60200-60200-60200
160437-60200-60200-60200
160282-60200-60200-60200
160306-60200-60200-60200
160511-60200-60200-60200
460681-60200-60200-60200
160280-60200-60200-60200
160223-60200-60200-60200
160271-60200-60200-60200
160275-60200-60200-60200
160325-60200-60200-60200
