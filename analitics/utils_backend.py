from analitics.models import Document


def check_file_in_base(filename):
    documents = Document.objects.all()
    for doc in documents:
        print(doc.name)
        if doc.name == filename:
            return False
    return True
