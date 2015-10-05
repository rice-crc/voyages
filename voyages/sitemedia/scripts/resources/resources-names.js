function submitWithValue(submitVal) {
    $('#form').append("<input type='hidden' name='action' value='" + submitVal + "' />");
    $("#form").submit();
    return false;
}

function retrieve_page(page_elem) {
    /* Enable the button with desired page to be submitted */
    $('#' + page_elem).prop('disabled', false);
    submitWithValue('requested_page');
    return false;
}

function sort_results(page_elem) {
    /* Enable the button with desired page to be submitted */
    $('#' + page_elem).prop('disabled', false);
    submitWithValue('sort_results');
    return false;
}