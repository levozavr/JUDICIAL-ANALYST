from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from analitics.models import Document, Json
from analitics.forms import DocumentForm
from analitics.parser.main import parse, documents
from datetime import datetime
import ast
import os


def load_models():
    for item in Json.objects.all():
        documents.append(ast.literal_eval(item.text))


load_models()


def check_file_in_base(filename):
    documents = Document.objects.all()
    for doc in documents:
        if doc.name == filename:
            return False, str(doc.docfile)
    return True, ''


def upload(request):
    form = DocumentForm(request.POST, request.FILES)
    if form.is_valid():
        if request.POST['pass'] != "123456":
            return render(request, 'analitics/update.html', {'form': form})
        check_file, filename = check_file_in_base(str(request.FILES['docfile']))
        if not check_file:
            return HttpResponseRedirect('/')
        newdoc = Document(docfile=request.FILES['docfile'], name=str(request.FILES['docfile']))
        newdoc.save()
        try:
            document = parse(str(newdoc.docfile))
        except Exception:
            os.remove('./media/' + str(newdoc.docfile))
            newdoc.delete()
            return HttpResponse(f"[ERROR {datetime.now()}]: Not right format of file")
        base_insert(document, newdoc)
        return HttpResponseRedirect('/')


def base_insert(doc, doc_model):
        js = Json(doc=doc_model, text=doc)
        js.save()
        with open('./tmp'+doc_model.name, 'w') as f:
            f.write(doc)

