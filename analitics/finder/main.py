from analitics.parser.main import parse, documents
from analitics.parser.utils import norm_form, clear_text, full_form, LinkFinder


parse('ых.txt')


def structure(text):
    text_ = norm_form(full_form(text))
    link = LinkFinder(text_).mining()

    return link


def search(text):
    text = structure(text)

    for doc in documents:
        for sol in doc['solutions']:
            for line in sol['lines']:
                for link in line['links']:
                    if link['essence'] == text['essence'] and link['number'] == text['number'] \
                            and link['document'] == text['document']:
                        print(link)


search(input('запрос:'))
