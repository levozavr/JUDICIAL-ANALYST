from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from analitics.models import Document
from analitics.forms import DocumentForm
from analitics.parser.main import parse, LINK

def check_file_in_base(filename):
    documents = Document.objects.all()
    for doc in documents:
        if doc.name == filename:
            return (False, str(doc.docfile))
    return (True, '')


def return_response(filename):
    parse(str(filename))
    res = LINK
    return HttpResponse(str(res))


def upload(request):
    form = DocumentForm(request.POST, request.FILES)
    if form.is_valid():
        check_file, filename = check_file_in_base(str(request.FILES['docfile']))
        if not check_file:
            return return_response(filename)
        newdoc = Document(docfile=request.FILES['docfile'], name=str(request.FILES['docfile']))
        newdoc.save()
        return return_response(str(newdoc.docfile))