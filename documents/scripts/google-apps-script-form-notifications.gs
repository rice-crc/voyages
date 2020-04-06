/**
 * On form submission, we send a summary to the Emory's voyages@emory.edu list.
 * The goal is to let everyone on the team be able to view the feedback submission.
 * Yang Li, yang.li@emory.edu 04/06/2020 Emory Center for Digital Scholarship
 */
function onFormSubmit(e) {  
  var values = e.namedValues;
  var htmlBody = "<style>table {  border-collapse: collapse;  width: 100%;}th, td {  padding: 8px;  text-align: left;  border-bottom: 1px solid #ddd;}</style>"
  htmlBody += "<div>A new Slave Voyages feedback submission has been received.</div> ";
  htmlBody += "<table>";
  htmlBody += "<tr><th>Question</th><th>Response</th></tr>";
  for (Key in values) {
    var label = Key;
    var data = values[Key];
    htmlBody += '<tr><td>' + label + '</td><td>' + data + '</td></tr>';
  };
  htmlBody += '</table>';
  htmlBody += "<p><a href='#'>View all submissions on Google Spreadsheet</a><p>";
  htmlBody += "<p>If you are looking for full access to this spreadsheet, please contact voyages@emory.edu for details. Thank you!</p>"
  htmlBody += "<p>This automated Email is sent through Google Apps Script made for Slave Voyages Feedback form under pastdata2020@gmail.com.</p>";
  GmailApp.sendEmail('voyages@emory.edu', 'Slave Voyages Feedback Submission', '', {htmlBody: htmlBody});
}