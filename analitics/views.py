from django.views.decorators.cache import cache_page
from analitics.utils_backend import *
from urllib.parse import unquote
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
    return render(request, 'analitics/search.html', {})


#TODO: name of project : judical analyst - judyst
#TODO: create issue for Tinkoff