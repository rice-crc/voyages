# Editing or adding new flatpages


## Requirements and structure

1. Requisite user privileges
	1. User must be set to is_staff=1 and is_superuser=1 in auth_user table to
	1. Log in to /admin/flatpages
	1. And add a flat page
1. Page hierarchy
	1. app given by first slash. examples:
		1. intra-american: /intra-essays/
		1. trans-atlantic: /essays/
		1. about: /about/
	1. subsection given by second slash. examples:
		1. intra-american: /intra-essays/intra-american-database-essays/
		1. trans-atlantic: /essays/research-notes/
		1. about pages:
			1. /about/about/
	1. order given by numbers. examples: 
		1. /essays/interpretation/a-brief-overview-of-the-trans-atlantic-slave-trade/0/
		1. /about/news/10/information-release-on-the-future-of-slave-voyages/0/
	1. language given by final character pair. examples:
		1. /about/acknowledgements/4/pt/
		1. /about/acknowledgements/4/en/

The short version:

* Find a page in the section you're working with
* Copy the url
* When creating a new page, paste that url in your page, and follow the format you see

Note: Caching can cause updates to the public site to be delayed up to 1 hour.

## News items special case

* Keep the FIRST number -- same for all news items
* Iterate the SECOND number -- +1 for each new news item
* The news feed on the front page will:
	* Capture all the news items (anything url with the format /about/about/news/10/TITLE/NUMBER/LANGUAGE)
	* Count backwards from the highest-numbered item
	* Display these left-to-right with the three highest-numbered items

Your body should look like this to get picked up in the news feed

	<div class="page-title-1">TITLE</div>
	<div class="method-info method-date">MONTH, YEAR</div>
	<p>HTML BODY PARAGRAPHS, FIRST PARAGRAPH MUST BE AT LEAST 200 CHARACTERS</p>
	...more p tags