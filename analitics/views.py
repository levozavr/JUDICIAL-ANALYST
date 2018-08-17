from django.views.decorators.cache import cache_page
from analitics.utils_backend import *
from urllib.parse import unquote
# Create your views here.


@cache_page(600)
def upload_file(request):
    # Handle file upload
    form = None
    if request.method == 'POST' and 'upload' in request.POST:
        return upload(request)
    elif request.method == 'POST' and 'analise' in request.POST:
        filename = unquote(unquote(request.POST['file'])).split('/media/')[1]
        nk, gk = parse(filename)
        return HttpResponse(f'удача!<br>упоминаний статей гражданского кодекса:{gk}<br>'
                            f'упоминаний статей налогового кодекса:{nk}')
    else:
        form = DocumentForm()

    documents = Document.objects.all()
    return render(request, 'analitics/index.html', {'documents': documents, 'form': form})