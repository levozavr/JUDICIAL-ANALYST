from analitics.parser.main import parse, documents
from analitics.parser.utils import norm_form, clear_text, full_form, LinkFinder


parse('ых.txt')


def structure(input):
    ess = ''
    num = []
    dok = ''
    input_ = norm_form(full_form(input))
    search_link = LinkFinder(input_).mining()
    for ess, num, dok in search_link:
        link = {'text': input, 'essence': ess, 'number': num, 'document': dok}
    return link


def search(input):
    input = structure(input)

    for doc in documents:
        for sol in doc['solutions']:
            for line in sol['lines']:
                for link in line['links']:
                    if link['essence'] == input['essence'] and link['number'] == input['number'] \
                            and link['document'] == input['document']:
                        print(link)


search(input('запрос:'))
