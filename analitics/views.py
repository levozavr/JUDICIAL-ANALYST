from django.views.decorators.cache import cache_page
from analitics.utils_backend import *
from analitics.finder.main import searcher_sols
# Create your views here.


@cache_page(0)
def upload_file(request):
    """
    function to upload document to base and make some prepossessing of it
    :param request: http request to this page Post or Get
    :return: http response of this page
    """
    try:
        if request.method == 'POST':
            return upload(request)
        else:
            form = DocumentForm()

        return render(request, 'analitics/update.html', {'form': form})
    except Exception:
        return HttpResponseRedirect('/update')


@cache_page(0)
def search(request):
    """
    function for loading main page and create a simple search by key words
    :param request: http request to this page Post or Get
    :return: http response of this page or redirect on page with results
    """
    try:
        if request.method == 'POST':
            try:
                search_str = request.POST['find']
                sols = searcher_sols(search_str)
            except Exception:
                sols = []
            if len(sols) == 0:
                return render(request, 'analitics/search.html', {'error': "We don't find anything..."})
            return HttpResponseRedirect(f'/result?link={search_str}')

        return render(request, 'analitics/search.html', {'error': ''})
    except Exception:
        return HttpResponseRedirect('/')


@cache_page(0)
def result(request):
    """
    function for loading page with results
    :param request: http get request
    :return: http response with results of searching
    """
    try:
        if request.method == 'GET' and 'link' in request.GET:
            if 'doc_name' in request.GET and 'sol_num' in request.GET:
                return give_text(request)
            return give_sols(request)

        return HttpResponseRedirect('/')
    except Exception:
        return HttpResponseRedirect('/')
