function FileBrowserPopup(callback, value, type) {
    var fbURL = '/admin/filebrowser/browse/?pop=5';
    fbURL = fbURL + "&type=" + type.filetype;
    if(value)
        fbURL += '&input=';
    const instanceApi = tinyMCE.activeEditor.windowManager.openUrl({
        title: 'Filebrowser image/media/file picker',
        url: fbURL,
        width: 1280,
        height: 800,
        onMessage: function(dialogApi, details) {
            callback(details.content);
            instanceApi.close();
        }
    });
    return false;
}

tinyMCE.init({
    mode : "specific_textareas",
    editor_selector : "tinymcetextareamanager",
	width: "1000px",
	height: "600px",
    theme_advanced_resizing : true,
    //images_upload_url: 'postAcceptor.php',
    plugins: [
        "advlist autolink lists link image charmap print preview hr anchor pagebreak",
        "searchreplace wordcount visualblocks visualchars code fullscreen",
        "insertdatetime media nonbreaking save table contextmenu directionality",
        "emoticons template paste textcolor"
    ],
    image_advtab: true,
    templates: [
        {title: 'Test template 1', content: 'Test 1'},
        {title: 'Test template 2', content: 'Test 2'}
    ],

    file_picker_callback: FileBrowserPopup,
});