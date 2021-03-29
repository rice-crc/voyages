Release 1.3
===========

Contribute App
--------------

This application running within Voyages allows users registered in the
site to contribute data to the project.
The other main component of this application is the editorial platform,
which is used by editors and reviewers to analyze and rectify the data
committed by users. After an editorial decision, a contribution may
be archived with no effect or it may be used to update the voyages
database by adding, modifying, merging, or deleting voyage records.

User Contribution Features
~~~~~~~~~~~~~~~~~~~~~~~~~~ 

* Users can log in to the site to contribute New voyages, Edit or Merge
  existing ones or suggest that some voyage should be Deleted.
* The contribution forms (except for Delete) are all shared with minor
  modifications that specialize to each type.
* The user can save a partial contribution and return to it later. All
  the unfinished contributions are listed in the user's main contribute
  page as a link. The user may also cancel the contribution (and that
  will delete it permanently from the system).
* In case of a New Voyage contribution, the user must include the source
  references used (this validation is enforced by the user interface
  and the backend code).
* In case of Edit/Merge contributions, the list of current source
  references is made available for comments (in which the user may
  specify editing or removing a reference). It is also possible to
  add new references.
* After finishing the work on a contribution, the user clicks on the
  'Review' button, which shows a read-only display of the entire
  contribution in summarized form. If an error is spotted, the user can
  return to editing the contribution. Otherwise, the contribution can
  be submitted for academic review.
* A committed contribution is still diplayed in the contributor's
  main page and the user is allowed to edit it until the time the
  contribution is picked up for review. After a review starts, the
  status of the contribution is changed to 'Under Review', blocking
  any further edits.

Editorial Platform
~~~~~~~~~~~~~~~~~~  

* After loging in, an editor is brought to the main editorial page, which
  presents a tabbed interface which allow the features described below.
* The list of pending contributions shows all user contributions that
  are not yet reviewed, are under revision, or having been marked as
  accepted or rejected. The only user contributions that are *not*
  displayed are those that have been published and those that have been
  explicitly Deleted.
* The editor may preview contributions, which allows a read-only view
  of the entire contribution. In this preview window, the editor can
  choose to assign a reviewer to the contribution, picking from the
  list of reviewers in the database and sending a message to the reviewer.
  This message is sent to the reviewer by e-mail, with a link that allows
  the reviewer to access the contribution (the reviewer can always access
  all the requests by logging in---these requests are shown in their main
  page).
* Once a review request is made (from the editor, to a reviewer), the
  contribution status is updated in the list. The editor can check the
  response given by the reviewer (if any) from this list. It is always
  possible for the editor to 'Archive a review request' if the reviewer
  is taking too long to accept/reject the work or if the review itself
  is not being done.
* The reviewer, after being notified by e-mail, can check the request
  by vistiting te link on the e-mail or simply by selecting the pending
  requests on their main Contribute page. The editor's message will
  be shown and a link to display the contribution preview is given.
  The reviewer has the option to reply by accepting or rejecting the
  assignment. 
* If the request is rejected, it will be removed from the list of pending
  requests and the status will be updated for the editor to see.
* If accepted, a copy of the entire interim data contributed by the
  user will be made and the reviewer will be allowed to modify any
  field values and or comment on the original contribution. The reviewer
  can see any pre-existing data (in case of Edit/Merge contributions)
  to quickly inspect the changes suggested by the contributor.
* The reviewer then provides a textual response to editor and a
  decision regarding the contribution. After the decision is made
  the request is removed from the reviewer's list and the status
  on the editor's list is updated to reflect the reviewer's decision.
* The editor may opt for skipping the reviewer assignment and instead 
  initiate an editorial review immediately.
* If a review has been made and submitted, the editor can start the
  editorial review.
* The editorial review makes a copy of all previous interim data,
  such as the user original contribution, the reviewer's input (if
  the reviewer has not been bypassed), and of course, the existing
  data in the system (in case of Edit/Merge contributions).
* If the fields agree in all versions, then it is marked as green.
  Otherwise, the individual values are marked in red. The editorial
  interim version is initialized to the original version of the
  data in this case. The conflicting values are clickable, with a
  single click being used to set the editor's value. The editor has
  a final say in the input and may override any field.
* In case there are suggestions for editing existing references,
  the editor may take action accordingly (a simple click shows
  a dialog with the Reference details in edit-mode).
* In case there are new source references, the editor must either
  delete them from the interim form explicitly or create the
  corresponding source in the database (in case the contribution 
  is to be accepted). Again, a simple click allows creating the
  source reference (with default values obtained from the contributed
  data). It is also necessary to specify a reference text, which
  is used to connect the Voyage that will be created/edited to
  the shared full Source Reference.
* The editor can write a message (for future reference) and make
  a decision regarding the contribution (accept, reject, delete).
  If delete is chosen, the contribution is archived and will not
  be shown in the list of pending contributions. If rejected, it
  will still appear in that list (with the status set as 'Rejected')
  until the time an editor decides to either reopen the case or
  delete it for good.
* In case of acceptance, the status is updated and the reviewed
  contribution will be listed in the Pending Publication tab.
* For new/merge voyages, a VoyageId must be specified by the
  editor before acceptance. This voyage id must be distinct from
  any existing id (except when the id is one of the voyages being
  merged in the contribution itself). Moreover, no other accepted
  contribution may be allocated the same id. All these restrictions
  are checked by the server code and error messages are shown
  to the editor when appropriate.
* The Downloads tab allows the editor to obtain a CSV file with
  all the contributions that match the status selections (made
  by ticking boxes). It is also possible to select for download
  the entire set of voyages in the database. The columns of the
  CSV match the SPSS format.
* The publication tab allows the editor to publish all the
  pending contributions. An optional action (highly recommended
  in production) is the full backup of the current data before
  the update. The process consists of three phases, the first
  is the optional backup (which may take several minutes),
  the second is the update on the voyages database by creating,
  modifying, and deleting records according to the accepted
  contributions pending publication. The third step is updating
  the Solr Index so that the voyages search is fresh. For 
  performance reasons, all voyages now have an update timestamp
  and the index is updated only for voyages for which the timestamp
  is recent.

Animated voyages map
--------------------

* Added support for complex source-destination routes over sea (previous
  version always used the globe geodesic between the two points).