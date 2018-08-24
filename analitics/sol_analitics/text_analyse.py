from analitics.parser.main import parse, documents

parse('ых.txt')

gkcount = 0
nkcount = 0
commoncount = 0

for doc in documents:
    for sol in doc['solutions']:
        print(sol['name'])
        for line in sol['lines']:
            for link in line['links']:
                    if link['document'] == ' гражданский  кодекс':
                        gkcount += 1
                    if link['document'] == ' налоговый  кодекс':
                        nkcount += 1
        print('Количество упоминаний ГК: ', gkcount)
        print('Количество упоминаний НК: ', nkcount)
        gkcount = 0
        nkcount = 0