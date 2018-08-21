from analitics.parser.utils import read_file_line_by_line, begin_module, end_module, clear_text, LinkFinder, logger
from analitics.parser.utils import Document, Link, Line, Solution, Place

#TODO: Ulyana try to rewrite this code more handsome, please
def parse(filename):
    """
    function that generate a special structure based on document
    :param filename: the way to the file in media folder
    :return: a data structure for the document
    """
    gen = read_file_line_by_line('./media/' + filename, code='cp1251')
    doc = Document(file_name=filename)
    document = [_ for _ in enumerate(gen)]
    dict_of_solution = {}

    for num_sol, solution in document:
        sol = Solution(sol_name=num_sol)
        for num_line, line in enumerate(solution.split('\n')):
            sol_line = Line(number=num_line, text=line)
            sol.add_line(line=sol_line)
        doc.add_solution(solution=sol)

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
                if begin_module.search(word) is not None and (num_begin == -1 or num_word-num_begin > 5):
                    num_begin = num_word
                if num_begin != -1 and end_module.search(word) is not None:
                    if num_word - num_begin < 19:
                        dict_of_solution[num_sol][num_line].append((num_begin, num_word))
                    num_begin = -1

    for key_sol, sol in dict_of_solution.items():
        for key_line, lines in sol.items():
            for line in lines:
                if len(line):
                    link_text = ''
                    if doc.get(key_sol).get(key_line).text == '':
                        continue
                    for num_word, word in enumerate(doc.get(key_sol).get(key_line).text.split(' ')):
                        if num_word >= line[0] and num_word <= line[1]:
                            link_text += word+' '
                    place = Place(doc_name=doc.name, sol_num=key_sol, line_num=line, begin=line[0], end=line[1])

                    result = LinkFinder(clear_text(link_text, hard=True)).mining()

                    if result:
                        for ess, num, dok in result:
                            link = Link(text=link_text, essence=ess, number=num, document=dok, place=place)

                            doc.put(key_sol, key_line, link)

                    else:
                        link = Link(text=link_text, essence='', number='', document='', place=place)
                        doc.put(key_sol, key_line, link)
    return doc
