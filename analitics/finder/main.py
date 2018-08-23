import analitics.parser.main as magic
from analitics.parser.utils import norm_form, full_form, LinkFinder


def structure(text):
    text_ = norm_form(full_form(text))
    search_link = LinkFinder(text_).mining()
    link = {'text': text, 'essence': search_link[0][0], 'number': search_link[0][1], 'document': search_link[0][2]}
    return link


def searcher(text):
    text = structure(text)
    links = []
    for doc in magic.documents:
        for sol in doc['solutions']:
            for line in sol['lines']:
                for link in line['links']:
                    if link['essence'] == text['essence'] and link['number'] == text['number'] \
                            and link['document'] == text['document']:
                        links.append(link)

    print(len(links))
    return links


