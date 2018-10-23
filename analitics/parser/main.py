from analitics.parser.utils import read_file_line_by_line, begin_module, end_module, clear_text, LinkFinder, full_form

"""a global list"""
documents = []


def create_dict_of_links(document, name):
    """
    create a carcase for difficult structure of doc
    :param document: text
    :param name: of this doc
    :return: structure of the doc
    """
    dict_of_links = {'name': name, 'solutions': []}
    for num_sol, solution in document:
        dict_of_links['solutions'].append({'number': num_sol, 'name': ' ', 'lines': []})
        for num_line, line in enumerate(solution.split('\n')):
            if num_line == 2 and num_sol != 0:
                dict_of_links['solutions'][num_sol]['name'] = line
            if num_line == 1 and num_sol == 0:
                dict_of_links['solutions'][num_sol]['name'] = line
            dict_of_links['solutions'][num_sol]['lines'].append({'number': num_line, 'text': line, 'links': []})
    return dict_of_links


def check_line(line, flag):
    """
    check then some rule of reading doc
    :param line: text to check
    :param flag: the latest condition
    :return: flag
    """
    if 'установил:' in line and not flag:
        return True
    if 'постановил:' in line or 'определил:' in line and flag:
        return False
    return flag


def create_dict_of_solutions(document):
    """
    fucntion that generate dict of solutions and links
    :param document: text
    :return: structure
    """
    dict_of_solution = {}
    dict_of_replace = {',': '', ' и ': ' ', ';': '', ':': ''}
    for num_sol, solution in document:
        dict_of_solution.update({num_sol: {}})
        flag_analyse = False
        for num_line, line in enumerate(solution.split('\n')):
            flag_analyse = check_line(line, flag_analyse)
            if not flag_analyse:
                continue
            dict_of_solution[num_sol].update({num_line: []})
            num_begin = -1
            for num_word, word in enumerate(line.split(' ')):
                word = clear_text(word, dict_of_replace)
                if begin_module.search(word) is not None and (num_begin == -1 or num_word-num_begin > 5):
                    num_begin = num_word
                if num_begin != -1 and end_module.search(word) is not None:
                    if num_word - num_begin < 19:
                        dict_of_solution[num_sol][num_line].append((num_begin, num_word))
                    num_begin = -1
    return dict_of_solution


#TODO: Ulyana try to rewrite this code more handsome, please
#TODO: add short forms of codex withot RF
def parse(filename):
    """
    function that generate a special structure based on document
    :param filename: the way to the file in media folder
    :return: none
    """
    #gen = read_file_line_by_line('./media/' + filename, code='cp1251')
    gen = read_file_line_by_line(filename, code='cp1251')
    name = filename.split('/')
    name = name[len(name)-1]
    document = [_ for _ in enumerate(gen)]
    dict_of_links = create_dict_of_links(document, name)
    dict_of_solution = create_dict_of_solutions(document)

    dict_of_replace = {',': '', ' и ': ' ', '(': '',
                       ')': '', ';': '', '-': ' ', ':': ''}
    for key_sol, sol in dict_of_solution.items():
        for key_line, lines in sol.items():
            for line in lines:
                if len(line):
                    link_text = ''
                    if dict_of_links['solutions'][key_sol]['lines'][key_line]['text'] == '':
                        continue
                    for num_word, word in enumerate(dict_of_links['solutions'][key_sol]
                                                    ['lines'][key_line]['text'].split(' ')):
                        if line[0] <= num_word <= line[1]:
                            link_text += word+' '
                    place = {'doc_name': name, 'sol_name': dict_of_links['solutions'][key_sol]['name'], 'sol_num': key_sol,
                             'line_num': key_line, 'begin': line[0], 'end': line[1]}
                    result = LinkFinder(clear_text(full_form(link_text.lower()), dict_of_replace)).mining()
                    if result:
                        for ess, num, dok in result:
                            link = {'text': link_text, 'essence': ess, 'number': num, 'document': dok, 'place': place}
                            dict_of_links['solutions'][key_sol]['lines'][key_line]['links'].append(link)

                    else:
                        link = {'text': link_text, 'essence': '', 'number': '', 'document': '', 'place': place}
                        dict_of_links['solutions'][key_sol]['lines'][key_line]['links'].append(link)
    documents.append(dict_of_links)
