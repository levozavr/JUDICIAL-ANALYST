import asyncio
import logging
import re
import pymorphy2


logging.basicConfig(
    format=u' %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.DEBUG,
    filename='manager.log')
logger = logging


@asyncio.coroutine
def read_file_line_by_line(file_name, code='utf-8'):
    """
    async generator to read file in with special delimeter
    :param file_name: the way to the file
    :param code: encoding of file (utf-8)
    :return: generator with all parts of file
    """
    with open(file_name, 'r', encoding=code) as f:
        while True:
            line = ''
            for l in f:
                if '------------------------------------------------------------------' in l:
                    break
                line += l
            if line == '' or line == '\n':
                break
            yield line
        logger.info('file read end now')
        yield 'stop'


def clear_text(text, hard=False):
    """
    delete from text special symbols
    :param text: text to clear
    :param hard: is it a hard clear?(False)
    :return: clear text
    """
    if hard:
        return text.lower().replace(',', '').replace(' и ', ' ').replace('(', '').\
            replace(')', '').replace(';', '').replace('-',' ')
    else:
        return text.lower().replace(',', '').replace(';', '').replace(':', '')


morph = pymorphy2.MorphAnalyzer()


def norm_form(link):
    """
    make all words in text initial form
    :param link: text to handle
    :return: text in initial form
    """
    new_link = []
    link = link.split(' ')
    for word in link:
        word = morph.parse(word)[0]
        new_link.append(word.normal_form)
    new_link = ' '.join(new_link)
    return new_link


begin_module = re.compile('^(\W)?((пункт|подпункт|част|раздел|подраздел|глав|стат|абзац)'
                          '(а|у|и|ой|ьей|ьёй|ью|ьям|ями|ям|ьями|ье|ом|ам|ах|е|ов|ей|ьях|ях|ьи|ья|ь|ы)?$|'
                          '^(ч|п|ст|пп|абз)(\.))$')

end_module = re.compile('^((федерац)(ия|ии|ий|иям|ию|ией|иями|иях))$|'
                        '^(рф)$|^(.*(фз))$|^(кодекс)(а|у|е|ом|ов|ами|ах|а|ы)(\W)?$')


class LinkFinder(object):
    def __init__(self, text):
        self.__text = text
        self.__essence = ''
        self.__numbers = []
        self.__document = ''
        self.__prefix_reg = []
        self.__numbers_reg = None
        self.__posfix_reg = []
        self.__is_it = True

    def __select_essence(self):
        text = self.__text
        for word in text.split(' '):
            for reg, name_ess in self.__prefix_reg:
                if reg.match(word) is not None:
                    self.__essence = name_ess+' '
                    self.__text = text.split(word)[1]
                    return None
        self.__is_it = False

    def __select_numbers(self):
        text = self.__text
        flag = False
        for word in text.split(' '):
            if self.__numbers_reg.match(word) is not None:
                if not flag:
                    flag = True
                self.__numbers.append(word)
            else:
                if flag:
                    break
        if flag:
            self.__text = text.split(self.__numbers[len(self.__numbers) - 1])[1]
        else:
            self.__numbers.append('')

    def __select_document(self):
        text = self.__text
        for word in text.split(' '):
            for reg, name_doc in self.__posfix_reg:
                if reg.match(word) is not None:
                    self.__document = text.split(word)[0]+' '+name_doc
                    return None
        self.__is_it = False

    def __set(self):
        self.__prefix_reg = [
            (re.compile('^(стат)''(а|у|и|ой|ьей|ьёй|ью|ьям|ям|ье|ом|ам|ах|е|ов|ей|ьях|ях|ьи|ья|ь|ы)?$|''^(ст)(\.)$'),
             'статья'),
            (re.compile('^(глав)''(а|у|и|ой|ьей|ьёй|ью|ьям|ям|ье|ом|ам|ах|е|ов|ей|ьях|ях|ьи|ья|ь|ы)?$'),
             'глава'),
            (re.compile('^(постановлени)(а|у|и|ой|ьей|ьёй|ью|ьям|ям|ье|ом|ам|ах|е|ов|ей|я|ях|ем)?$'),
             'постановления')
        ]
        self.__numbers_reg = re.compile('([0-9]+)')
        self.__posfix_reg = [
            (re.compile('^(кодекс)(а|у|е|ом|ов|ами|ах|а|ы)?(\W)?$'),
             'кодекс'),
            (re.compile('^(.*(фз))$'),
             'фз')
        ]

    def mining(self):
        """
        function what finding links in text
        :return: a list of links
        """
        self.__set()
        self.__select_essence()
        if self.__is_it:
            self.__select_numbers()
        if self.__is_it:
            self.__select_document()
        if not self.__is_it:
            return None
        return [(self.__essence, num, norm_form(self.__document)) for num in self.__numbers]


class Place(object):
    def __init__(self, doc_name, sol_num, line_num, begin, end):
        self.doc_name = doc_name
        self.sol_num = sol_num
        self.line_num = line_num
        self.begin = begin
        self.end = end


class Link(object):
    def __init__(self, text, essence, number, document, place):
        self.text = text
        self.essential = essence
        self.number = number
        self.document = document
        self.place = place


class Line(object):
    def __init__(self, number, text, links=[]):
        self.number = number
        self.links = links
        self.text = text

    def add_link(self, link):
        self.links.append(link)

    def add_links(self, links):
        self.links += links


class Solution(object):
    def __init__(self,  sol_name, lines={}):
        self.sol_name = sol_name
        self.lines = lines

    def add_line(self, line):
        self.lines.update({line.number: line})

    def get(self, num):
        res = self.lines.get(num)
        if res:
            return res
        return Line(number=num, text='')

    def put(self,key_line,link):
        self.lines[key_line].add_link(link)


class Document(object):
    def __init__(self, file_name, solutions={}):
        self.name = file_name
        self.solutions = solutions

    def add_solution(self, solution):
        self.solutions.update({solution.sol_name: solution})

    def get(self, num):
        res = self.solutions.get(num)
        if res:
            return res
        return Solution(sol_name=num)

    def put(self, key_sol, key_line, link):
        self.solutions[key_sol].put(key_line, link)
