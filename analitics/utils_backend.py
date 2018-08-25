from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from analitics.models import Document
from analitics.forms import DocumentForm
from analitics.parser.main import parse
import analitics.parser.main as magic
from datetime import datetime
from analitics.finder.main import searcher_sols, searcher_links
import os


def load_models():
    """
    function for loading text models when server starts
    :return: None
    """
    try:
        for item in Document.objects.all():
            parse(str(item.docfile))
    except Exception:
        print(f"[ERROR {datetime.now()}] no models was loaded")


"""loading models"""
load_models()


def check_file_in_base(filename):
    """
    function that checs is any file in base or not
    :param filename: name of the file
    :return: True and way to this file or False an ''
    """
    documents_ = Document.objects.all()
    for doc in documents_:
        if doc.name == filename:
            return False, str(doc.docfile)
    return True, ''


def upload(request):
    """
    logic of view-function that upload file
    :param request: http request
    :return: http response
    """
    form = DocumentForm(request.POST, request.FILES)
    if form.is_valid():
        if request.POST['pass'] != "123456":
            return render(request, 'analitics/update.html', {'form': form})
        check_file, filename = check_file_in_base(str(request.FILES['docfile']))
        if not check_file:
            return HttpResponseRedirect('/')
        newdoc = Document(docfile=request.FILES['docfile'], name=str(request.FILES['docfile']))
        try:
            newdoc.save()
        except Exception:
            return HttpResponse(f"[ERROR {datetime.now()}]: Not right name of file please use unicode encoding")
        try:
            parse(str(newdoc.docfile))
        except Exception:
            os.remove('./media/' + str(newdoc.docfile))
            newdoc.delete()
            return HttpResponse(f"[ERROR {datetime.now()}]: Not right format of file")
        return HttpResponseRedirect('/')


def give_sols(request):
    """
    part of logic view function to demonstrate results
    :param request: http request
    :return: http response
    """
    try:
        search_str = request.GET['link']
        sols = searcher_sols(search_str)
    except Exception:
        return HttpResponse(f"[ERROR {datetime.now()}]: Please don't use api with out interface")
    answer = []
    for sol in sols:
        ans = {'href': f"/result?doc_name={sol['doc_name']}&sol_num={sol['number']}&link={search_str}",
               'text': sol['name']}
        answer.append(ans)
    return render(request, 'analitics/result.html', {'sols': answer})


def give_text(request):
    """
    part of logic view function to demonstrate results
    :param request: http request
    :return: http response
    """
    try:
        sol_num = request.GET['sol_num']
        doc_name = request.GET['doc_name']
        links = searcher_links(request.GET['link'], sol_num, doc_name)
        print(links)
        for doc in magic.documents:
            if doc['name'] == doc_name:
                ans = []
                for num_line, line in enumerate(doc['solutions'][int(sol_num)]['lines']):
                    for num, word in enumerate(line['text'].split(' ')):
                        color_start = None
                        color_stop = None
                        for link in links:
                            if link['num_line'] == num_line and link['begin'] == num:
                                color_start = 1
                            if link['num_line'] == num_line and link['end'] == num:
                                color_stop = 1
                        ans.append({"word": word, "color_start": color_start, 'color_end': color_stop, "end": None})
                    ans.append({"word": None, "color_start": None, 'color_end': None, "end": 1})
                return render(request, 'analitics/solution.html',
                              {'text': ans, 'links': links, 'name': doc['solutions'][int(sol_num)]['name']})
        return HttpResponseRedirect('/')
    except Exception:
        return HttpResponse(f"[ERROR {datetime.now()}]: Please don't use api with out interface")
