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

tinymce.init({
    selector: "textarea",
    plugins: "link image media",
//     images_upload_url: '/documents/blog/images/',
    image_advtab: true,
    file_picker_callback: FileBrowserPopup,
});
