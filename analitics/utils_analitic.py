from yargy import (
    Parser,
    rule,
    and_, or_
)
from yargy.pipelines import morph_pipeline
from yargy.interpretation import fact, attribute
from yargy.predicates import (
    eq, gte, lte, length_eq,
    dictionary, normalized,
)

NUM = and_(gte(1), lte(1000))

NUMBERS = rule(NUM,
               rule(eq(','), NUM).repeatable().optional())

Entry = fact(
    'Entry',
    ['type', 'numbers']
)

GK = rule(
    or_(rule(normalized('статья')),
        rule('ст', eq('.').optional())
        ),
    NUMBERS.interpretation(Entry.numbers),
    morph_pipeline({
        'гк',
        'гражданский кодекс',
    }).interpretation(Entry.type.const('ГК')),

).interpretation(Entry)

NK = rule(
    or_(rule(normalized('статья')),
        rule('ст', eq('.').optional())
        ),
    NUMBERS.interpretation(Entry.numbers),
    morph_pipeline({
        'нк',
        'налоговый кодекс',
    }).interpretation(Entry.type.const('НК')),

).interpretation(Entry)


def counter(text, codex):
    global countGK
    global generalGK
    global countNK
    global generalNK

    for s in range(len(text)):
        a = list(text[s])
        b = ''.join(a)
        # print(b)
        if codex == 'гк':
            countGK += (len([int(l) for l in b.split() if l.isdigit()]) - 1)
        elif codex == 'нк':
            countNK += (len([int(l) for l in b.split() if l.isdigit()]) - 1)
    generalGK += countGK
    generalNK += countNK


def analyze(text):
    global countNK
    global countGK

    for j in text.split('\n'):
        if (re.search(pattern1, j) is not None) or (re.search(pattern3, j) is not None):
            text1 = re.findall(pattern1, j)
            text3 = re.findall(pattern3, j)
            counter(text1, 'гк')
            counter(text3, 'гк')
        elif (re.search(pattern2, j) is not None) or (re.search(pattern4, j) is not None):
            text2 = re.findall(pattern2, j)
            text4 = re.findall(pattern4, j)
            counter(text2, 'нк')
            counter(text4, 'нк')
    countGK = 0
    countNK = 0


def parse(contents):
    global generalGK
    generalGK = 0
    global generalNK
    generalNK = 0


    contents = contents.lower().replace(',', '')
    for solution in contents.split('------------------------------------------------------------------'):
        if solution.find('установил:') == -1 or solution.find('постановил:') == -1:
            continue
        solution_parse = solution.split('установил:')[1]
        solution_parse = solution_parse.split('постановил:')[0]
        analyze(solution_parse)
    return (generalNK, generalGK)


if __name__ == '__main__':

    with open('лёва.txt') as file:
        contents = file.read()

    print(parse(contents))

    NUM = and_(gte(1), lte(1000))

    NUMBERS = rule(NUM,
                   rule(eq(','), NUM).repeatable().optional())

    Entry = fact(
        'Entry',
        ['type', 'numbers']
    )

    GK = rule(
        or_(rule(normalized('статья')),
            rule('ст', eq('.').optional())
            ),
        NUMBERS.interpretation(Entry.numbers),
        morph_pipeline({
            'гк',
            'гражданский кодекс',
        }).interpretation(Entry.type.const('ГК')),

    ).interpretation(Entry)

    NK = rule(
        or_(rule(normalized('статья')),
            rule('ст', eq('.').optional())
            ),
        NUMBERS.interpretation(Entry.numbers),
        morph_pipeline({
            'нк',
            'налоговый кодекс',
        }).interpretation(Entry.type.const('НК')),

    ).interpretation(Entry)


    for match in Parser(GR).findall('лёва.txt'):
        print(match.fact)
