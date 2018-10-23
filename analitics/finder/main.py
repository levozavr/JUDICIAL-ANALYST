import analitics.parser.main as magic
from analitics.parser.utils import norm_form, full_form, LinkFinder


def structure(text):
    """
    function what get a structure of the link in search request
    :param text: text with link
    :return: link structure
    """
    text_ = norm_form(full_form(text))
    search_link = LinkFinder(text_).mining()
    link = {'text': text, 'essence': search_link[0][0], 'number': search_link[0][1], 'document': search_link[0][2]}
    return link


def searcher_links(text, sol_number, doc_name):
    """
    function to find links in one solution in one doc
    :param text: search request
    :param sol_number: number of the solution
    :param doc_name: name of the document
    :return: list of links
    """
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
    """
    function that find a sols there are this link
    :param text: search request
    :return: list of solutions
    """
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
