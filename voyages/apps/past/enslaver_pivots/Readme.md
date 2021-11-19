## iam_to_enslavers.py

* walks through the captain and owner tables
* pulls some minimal, associated voyage data (year,embarkation & disembarkation ports)
* creates entries with
	* name
	* unique id based on: current mysql rowid, enslaver role, and an IAM prefix
	* first year, last year of associated voyages
* creates a corresponding entry in the alias table and links back to the enslaver identity entry
* reestablishes the link with the voyage

ran it successfully with: 0012_auto_20211119_0213.py