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
    error = ''
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            if not check_file_in_base(str(request.FILES['docfile'])):
                error = 'Файл с таким названием уже загружен'
                form = DocumentForm()  # A empty, unbound form
                documents = Document.objects.all()
                return render(request, 'analitics/index.html', {'documents': documents, 'form': form, 'error': error})
            newdoc = Document(docfile=request.FILES['docfile'], name=str(request.FILES['docfile']))
            newdoc.save()
            nk, gk = parse(str(newdoc.docfile))
            return HttpResponse(f'удача!<br>упоминаний статей гражданского кодекса:{gk}<br>'
                                f'упоминаний статей налогового кодекса:{nk}')
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form

    return render(request,'analitics/index.html',{'documents': documents, 'form': form, 'error': error})