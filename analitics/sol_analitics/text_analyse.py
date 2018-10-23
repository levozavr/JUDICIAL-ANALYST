from analitics.parser.main import parse, documents

parse('ых.txt')

gk = 0
apk = 0
nk = 0
tk = 0
gpk = 0
bk = 0
kas = 0
zk = 0
koap = 0
lk = 0
tkeas = 0
uik = 0
upk = 0
gik = 0
kzot = 0
sk = 0
tkts = 0
uk = 0
commoncount = 0

dict_of_codex = {' арбитражно процессуальный  кодекс': apk, ' налоговый  кодекс': nk, ' гражданский  кодекс': gk, ' трудовой  кодекс': tk,
                 ' гражданский процессуальный  кодекс': gpk, ' бюджетный  кодекс': bk, ' жилищный  кодекс': gik,
                 ' кодекс административного судопроизводства': kas, ' земельный  кодекс': zk, ' кодекс законов о труде': kzot,
                 ' кодекс об административных правонарушениях': koap, ' лесной  кодекс': lk, ' семейный  кодекс': sk,
                 ' таможенный кодекс евразийского экономического союза': tkeas, ' таможенный кодекс таможенного союза': tkts,
                 ' уголовно исполнительный  кодекс': uik, ' уголовно процессуальный  кодекс ': upk, ' уголовный  кодекс': uk
                 }


for doc in documents:
    for sol in doc['solutions']:
        for line in sol['lines']:
            for link in line['links']:
                if link['document'] in dict_of_codex:
                    dict_of_codex[link['document']] += 1
            codex = []
        for key, value in dict_of_codex.items():
            if dict_of_codex[key] != 0:
                codex.append((key, dict_of_codex[key]))
            dict_of_codex[key] = 0
        if codex != []:
            print(sol['name'])
            print(codex, '\n')



