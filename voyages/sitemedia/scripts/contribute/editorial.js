function beginEditorialReview(contribution_id) {
    $.ajax({
        url: '/contribute/begin_editorial_review',
        method: 'POST',
        data: {
            contribution_id: contribution_id
        },
        error: function() {
            alert(gettext("A server error occurred, please contact the IT department"));
        },
        success: function(data) {
            var url = 'contribute/editorial_review/' + data.editor_contribution_id;
        }
    })    
}