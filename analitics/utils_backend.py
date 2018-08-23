from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from analitics.models import Document, Json
from analitics.forms import DocumentForm
from analitics.parser.main import parse
import analitics.parser.main as magic
from datetime import datetime
from analitics.finder.main import searcher
import ast
import os


def load_models():
    for item in Json.objects.all():
        magic.documents.append(ast.literal_eval(item.text))


load_models()


def check_file_in_base(filename):
    documents_ = Document.objects.all()
    for doc in documents_:
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


def give_links(request):
    try:
        search_str = request.GET['link']
        links = searcher(search_str)
    except Exception:
        return HttpResponse(f"[ERROR {datetime.now()}]: Please don't use api with out interface")
    answer = []
    for link in links:
        ans = {'href': f"/result?doc_name={link['place']['doc_name']}&sol_num={link['place']['sol_num']}"}
        ans.update({'text': link['text']})
        answer.append(ans)
    return render(request, 'analitics/result.html', {'links': answer})


def give_solutions(request):
    try:
        sol_num = request.GET['sol_num']
        doc_name = request.GET['doc_name']
        for doc in magic.documents:
            if doc['name'] == doc_name:
                ans = []
                for line in doc['solutions'][int(sol_num)]['lines']:
                    ans.append(line['text'])
                return render(request, 'analitics/solution.html',
                              {'text': ans, 'name': doc['solutions'][int(sol_num)]['name']})

    except Exception:
        return HttpResponse(f"[ERROR {datetime.now()}]: Please don't use api with out interface")
