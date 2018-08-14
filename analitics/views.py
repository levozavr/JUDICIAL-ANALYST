from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from analitics.models import Document
from analitics.forms import DocumentForm
from analitics.utils import parse
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")


def upload_file(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
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
    return render(request,'analitics/index.html',{'documents': documents, 'form': form})