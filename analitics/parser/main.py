from analitics.parser.utils import read_file_line_by_line, begin_module, end_module, clear_text, Link,logger

LINK = []


def parse(filename):
    gen = read_file_line_by_line('./media/' + filename, code='cp1251')

    document = [_ for _ in enumerate(gen)]
    dict_of_solution = {}
    dict_of_text = {}

    for num_sol, solution in document:
        dict_of_text.update({num_sol: {}})
        for num_line, line in enumerate(solution.split('\n')):
            dict_of_text[num_sol].update({num_line: line})

    for num_sol, solution in document:
        dict_of_solution.update({num_sol: {}})
        flag_analyse = False
        for num_line, line in enumerate(solution.split('\n')):
            if 'установил:' in line:
                flag_analyse = True
            if 'постановил:' in line or 'определил:' in line:
                flag_analyse = False
            if not flag_analyse:
                continue
            dict_of_solution[num_sol].update({num_line: []})
            num_begin = -1
            for num_word, word in enumerate(line.split(' ')):
                word = clear_text(word)
                if begin_module.search(word) is not None and (num_begin == -1 or num_word-num_begin > 6):
                    num_begin = num_word
                if num_begin != -1 and end_module.search(word) is not None:
                    if num_word - num_begin < 19:
                        dict_of_solution[num_sol][num_line].append((num_begin, num_word))
                    num_begin = -1

    for key_sol, sol in dict_of_solution.items():
        for key_line, lines in sol.items():
            for line in lines:
                if len(line):
                    link = ''
                    for num_word, word in enumerate(dict_of_text[key_sol][key_line].split(' ')):
                        if num_word >= line[0] and num_word <= line[1]:
                            link += word+' '
                    res = link+' ' + str(Link(clear_text(link, hard=True)).mining())+' <br>'
                    LINK.append(res)
    return LINK


