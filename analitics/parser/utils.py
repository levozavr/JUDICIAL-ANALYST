import asyncio
import logging
import re
import pymorphy2

logging.basicConfig(
    format=u' %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.DEBUG,
    filename='manager.log')
logger = logging

dict_of_short = {'апк': 'арбитражно процессуальный кодекс', 'нк': 'налоговый кодекс', 'гк': 'гражданский кодекс', 'тк': 'трудовой кодекс',
                 'гпк': 'гражданский процессуальный кодекс', 'бк': 'бюджетный кодекс', 'жк': 'жилищный кодекс',
                 'кас': 'кодекс административного судопроизводства', 'зк': 'земельный кодекс', 'кзот': 'кодекс законов о труде',
                 'коап': 'кодекс об административных правонарушениях', 'лк': 'лесной кодекс', 'cк': 'семейный кодекс',
                  'тк еаэс': 'таможенный кодекс евразийского экономического союза', 'тк тс': 'таможенный кодекс таможенного союза',
                 'уик': 'уголовно исполнительный кодекс', 'упк': 'уголовно процессуальный кодекс ', 'ук': 'уголовный кодекс', 'ст': 'статья',
                 'ст.': 'статья', 'абз':  'абзац', 'абз.': 'абзац', 'гл.': 'глава', 'гл': 'глава'
                 }


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


def clear_text(text, dict):
    """
    func-deleter of special symbols
    :param text: input string
    :param dict: dictionary of delimeters
    :return: clear text
    """
    new_text = ''
    text = text.lower()

    for key, values in dict.items():
            text = text.replace(key, values)
    new_text = new_text + text

    return new_text


def full_form(text):
    """
    function changes short form for a long form
    :param text: text to change
    :return: changed text
    """
    new_text = ''
    for word in text.lower().split(' '):
        if word in dict_of_short:
            for key, values in dict_of_short.items():
                word = word.replace(key, values)
        new_text = new_text + word + ' '

    return new_text


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
                          '(а|у|ой|ам|ах|е|ы|ами|ьей|ьёй|ью|ьям|ье|ьях|ьи|ья|ей|ьями|ов|ев|ь|ом|ем|и|ям|ями|ях)?$|'
                          '^(ч|п|ст|пп|абз)(\.))$')

end_module = re.compile('^((федерац)(ия|ии|ий|иям|ию|ией|иями|иях))$|'
                        '^(рф)$|^(.*(фз))$|^(кодекс)(а|у|е|ом|ов|ами|ах|а|ы)(\W)?$')


class LinkFinder(object):
    """
    class to find a structure of link
    """
    def __init__(self, text):
        """
        init a class
        :param text: text with link
        """
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
            (re.compile('^(стат)''(ьей|ьёй|ью|ьям|ье|ьях|ьи|ья|ей|ьями)?$|''^(ст)(\.)$'),
             'статья'),
            (re.compile('^(глав)''(а|у|ой|ам|ах|е|ы|ами)?$'),
             'глава'),
            (re.compile('^(постановлени)(и|ям|е|я|ях|ем|й|ю|ями)?$'),
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

