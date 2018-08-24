from django.views.decorators.cache import cache_page
from analitics.utils_backend import *
from analitics.finder.main import searcher_sols
# Create your views here.


@cache_page(0)
def upload_file(request):
    # Handle file upload
    if request.method == 'POST':
        return upload(request)
    else:
        form = DocumentForm()

    return render(request, 'analitics/update.html', {'form': form})


@cache_page(0)
def search(request):
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


@cache_page(0)
def result(request):
    if request.method == 'GET' and 'link' in request.GET:
        if 'doc_name' in request.GET and 'sol_num' in request.GET:
            return give_text(request)
        return give_sols(request)

    return HttpResponseRedirect('/')
