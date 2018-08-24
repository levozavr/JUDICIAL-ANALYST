from analitics.parser.utils import read_file_line_by_line, begin_module, end_module, clear_text, LinkFinder, logger, full_form

documents = []

#TODO: Ulyana try to rewrite this code more handsome, please
#TODO: add short forms of codex withot RF
def parse(filename):
    """
    function that generate a special structure based on document
    :param filename: the way to the file in media folder
    :return: a data structure for the document
    """
    #gen = read_file_line_by_line('./media/' + filename, code='cp1251')
    gen = read_file_line_by_line(filename, code='cp1251')
    name = filename.split('/')
    name = name[len(name)-1]
    document = [_ for _ in enumerate(gen)]
    dict_of_links = {'name': name, 'solutions': []}
    dict_of_solution = {}

    for num_sol, solution in document:
        dict_of_links['solutions'].append({'number': num_sol, 'name': '', 'lines': []})
        for num_line, line in enumerate(solution.split('\n')):
            dict_of_links['solutions'][num_sol]['lines'].append({'number': num_line, 'text': line, 'links': []})

    dict_of_replace = {',': '', ' и ': ' ', ';': '', ':': ''}
    for num_sol, solution in document:
        dict_of_solution.update({num_sol: {}})
        flag_analyse = False
        for num_line, line in enumerate(solution.split('\n')):
            if num_line == 2:
                dict_of_links['solutions'][num_sol]['name'] = line
            if 'установил:' in line:
                flag_analyse = True
            if 'постановил:' in line or 'определил:' in line:
                flag_analyse = False
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
                    place = {'doc_name': name, 'sol_num': key_sol,
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
    return str(dict_of_links)
