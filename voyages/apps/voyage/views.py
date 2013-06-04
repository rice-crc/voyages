from django.http import Http404, HttpResponseRedirect
from django.template import TemplateDoesNotExist, Context, loader, RequestContext
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from os import listdir
from .forms import UploadFileForm

def get_page(request, chapternum, sectionnum, pagenum):
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    pagepath = "voyage/c" + chapternum + "_s" + sectionnum + "_p" + pagenum + ".html"
    templatename = "voyage/c" + chapternum + "_s" + sectionnum + "_generic" + ".html"
    return render_to_response(templatename, {},
                              context_instance=RequestContext(request, {"pagepath" : pagepath}));

@staff_member_required
def download_file(request):
    '''
    This view serves uploading files, which will be in 
    the download section. It uses UploadFileForm to maintain
    information regarding uploaded files and call 
    handle_uploaded_file() to store files on the disk.
    This view is available only for admin users.
    '''
    templatename = 'voyage/upload.html'

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['downloadfile'])
            return HttpResponseRedirect('/admin/downloads')
    else:
        form = UploadFileForm()
    uploaded_files = listdir(settings.MEDIA_ROOT + '/download')
    return render_to_response(templatename, {'form': form, 'uploaded_files': uploaded_files},
                context_instance=RequestContext(request))

def handle_uploaded_file(f):
    '''
    Function handles uploaded files by saving them
    by chunks in the MEDIA_ROOT/download directory
    '''
    with open('%s/%s/%s' % (settings.MEDIA_ROOT, 'download', f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

