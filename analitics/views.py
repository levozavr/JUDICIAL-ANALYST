from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from analitics.models import Document
from analitics.forms import DocumentForm
from analitics.utils_analitic import parse
from  analitics.utils_backend import *
# Create your views here.


def upload_file(request):
    # Handle file upload
    form = None
    if request.method == 'POST' and 'upload' in request.POST:
        return upload(request)
    elif request.method == 'POST' and 'analise' in request.POST:
        print(str(request.FILES['docfile']))
    else:
        form = DocumentForm()

    documents = Document.objects.all()

    return render(request, 'analitics/index.html', {'documents': documents, 'form': form})