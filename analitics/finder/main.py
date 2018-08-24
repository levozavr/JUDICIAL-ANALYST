import analitics.parser.main as magic
from analitics.parser.utils import norm_form, full_form, LinkFinder


def structure(text):
    text_ = norm_form(full_form(text))
    search_link = LinkFinder(text_).mining()
    link = {'text': text, 'essence': search_link[0][0], 'number': search_link[0][1], 'document': search_link[0][2]}
    return link


def searcher_links(text, sol_number, doc_name):
    text = structure(text)
    links = []
    for doc in magic.documents:
        if doc['name'] != doc_name:
            continue
        for line in doc['solutions'][int(sol_number)]['lines']:
            for link in line['links']:
                if link['essence'] == text['essence'] and link['number'] == text['number'] \
                        and link['document'] == text['document']:
                    links.append({'begin': link['place']['begin'], 'end': link['place']['end'],
                                  'num_line': link['place']['line_num']})
    return links


def searcher_sols(text):
    text = structure(text)
    sols = []
    for doc in magic.documents:
        for sol in doc['solutions']:
            flag = False
            for line in sol['lines']:
                if flag:
                    break
                for link in line['links']:
                    if link['essence'] == text['essence'] and link['number'] == text['number'] \
                            and link['document'] == text['document']:
                        sols.append({'number': sol['number'], 'name': sol['name'], 'doc_name': doc['name']})
                        flag = True
                        break
    return sols
