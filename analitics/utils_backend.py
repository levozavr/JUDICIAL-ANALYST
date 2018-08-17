from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from analitics.models import Document
from analitics.forms import DocumentForm
from analitics.utils_analitic import parse

def check_file_in_base(filename):
    documents = Document.objects.all()
    for doc in documents:
        if doc.name == filename:
            return (False, str(doc.docfile))
    return (True, '')


def upload(request):
    form = DocumentForm(request.POST, request.FILES)
    if form.is_valid():
        check_file, filename = check_file_in_base(str(request.FILES['docfile']))
        if not check_file :
            nk, gk = parse(str(filename))
            return HttpResponse(f'удача!<br>упоминаний статей гражданского кодекса:{gk}<br>'
                                f'упоминаний статей налогового кодекса:{nk}')
        newdoc = Document(docfile=request.FILES['docfile'], name=str(request.FILES['docfile']))
        newdoc.save()
        nk, gk = parse(str(newdoc.docfile))
        return HttpResponse(f'удача!<br>упоминаний статей гражданского кодекса:{gk}<br>'
                            f'упоминаний статей налогового кодекса:{nk}')