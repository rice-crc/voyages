from django.http import Http404, HttpResponseRedirect
from django import forms
from django.template import TemplateDoesNotExist, loader, RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from os import listdir, stat
from stat import ST_SIZE, ST_MTIME
from hurry.filesize import size
import time
from .forms import UploadFileForm
from .models import *


def get_page(request, chapternum, sectionnum, pagenum):
    """
    Voyage Understanding the Database part
    
    Display an html page corresponding to the chapter-section-page passed in
    ** Context **
    ``RequestContext``
    
    ** Basic template that will be rendered **
    :template:`voyage/c01_s02_generic.html`
    
    Further content is rendered using the pagepath parameter 
    """
    # We might want to do some error checking for pagenum here. Even though 404 will be raised if needed
    pagepath = "voyage/c" + chapternum + "_s" + sectionnum + "_p" + pagenum + ".html"
    templatename = "voyage/c" + chapternum + "_s" + sectionnum + "_generic" + ".html"
    try:
        loader.get_template(pagepath)
        loader.get_template(templatename)
        return render_to_response(templatename, {},
                              context_instance=RequestContext(request, {"pagepath" : pagepath}))
    except TemplateDoesNotExist:
        raise Http404

@staff_member_required
def download_file(request):
    """
    This view serves uploading files, which will be in 
    the download section. It uses UploadFileForm to maintain
    information regarding uploaded files and call 
    handle_uploaded_file() to store files on the disk.
    This view is available only for admin users.
    :template:`voyage/upload.html`
    """
    templatename = 'voyage/upload.html'

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['downloadfile'])
            return HttpResponseRedirect('/admin/downloads')
    else:
        form = UploadFileForm()
    uploaded_files = listdir(settings.MEDIA_ROOT + '/download')
    uploaded_files_info =[]
    for f in uploaded_files:
        st = stat(settings.MEDIA_ROOT + '/download/' + f)
        uploaded_files_info.append({'name': f, 'size': size(st[ST_SIZE]), 'date_mod': time.asctime(time.localtime(st[ST_MTIME]))})

    return render_to_response(templatename, {'form': form, 'uploaded_files': uploaded_files_info},
                context_instance=RequestContext(request))

def handle_uploaded_file(f):
    """
    Function handles uploaded files by saving them
    by chunks in the MEDIA_ROOT/download directory
    """
    with open('%s/%s/%s' % (settings.MEDIA_ROOT, 'download', f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def search(request):
    """
    Currently on renders the initial page
    """
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    return render_to_response("voyage/search.html", {},
                context_instance=RequestContext(request))


def search(request, added_field):
    if request.method == 'POST':
        if not request.GET('form:attr_selected') is None:
            pass
    elif request.method == 'GET':
        pass
    return render_to_response("voyage/search.html", {},
                context_instance=RequestContext(request))

def get_var_box(request, varname):

    # Return/construct a box with information about the variables:
    list_text_fields = ['basic_ship_name', 'basic_owner',]
    list_select_fields = ['basic_nationality', 'basic_outcome_slaves',
                          'basic_outcome_owner', 'basic_outcome_resistance']
    list_numeric_fields = ['var_voyage_id']

    if varname in list_text_fields:
        # Plain text fields
        input_field_name = "input_" + varname
        return render_to_response("voyage/search_box_plain_text.html",
                {'varname': varname, 'input_field_name' : input_field_name},
                context_instance=RequestContext(request))
    elif varname in list_select_fields:
        # Select box variables
        choices = getChoices(varname)
        varname_wrapper = "select_" + varname
        quicksearch_field = "qs_" + varname
        return render_to_response("voyage/search_box_select.html",
                {'varname': varname, 'choices': choices,
                 'varname_wrapper' : varname_wrapper,},
                context_instance=RequestContext(request))
    elif varname in list_numeric_fields:
        # Numeric variables
        return render_to_response("voyage/search_box_numeric.html", {'varname': varname},
                context_instance=RequestContext(request))
    else:
        pass

def getChoices(varname):
    choices = []
    if varname in ['basic_nationality', ]:
        for nation in Nationality.objects.all():
            choices.append({'choice_id': nation.pk, 'choice_text': nation.label })
    elif varname in ['basic_outcome_slaves',]:
        for outcome in ParticularOutcome.objects.all():
            choices.append({'choice_id': outcome.pk, 'choice_text': outcome.label })
    elif varname in ['basic_outcome_owner',]:
        for outcome in OwnerOutcome.objects.all():
            choices.append({'choice_id': outcome.pk, 'choice_text': outcome.label })
    elif varname in ['basic_outcome_resistance',]:
        for outcome in Resistance.objects.all():
            choices.append({'choice_id': outcome.pk, 'choice_text': outcome.label })
    return choices