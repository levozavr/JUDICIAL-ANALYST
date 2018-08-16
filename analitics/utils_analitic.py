import re
import yargy
from yargy import and_

arrNK = []
arrGK = []

countGK = 0
countNK = 0
obshiycountGK = 0
obshiycountNK = 0


pattern1 = '(\W)((стат)(ья|ьи|ье|ей|ёй|ьей|ьёй|ьях)+)(((\s)[0-9]{1,5}(,)?)+)' \
           '(\s)(гражданск)(ий|ого|им|ому|ом)(\s)(кодекс)(а|у|е|ом)+'
pattern2 = '(\W)((стат)(ья|ьи|ье|ей|ёй|ьей|ьёй|ьях)+)(((\s)[0-9]{1,5}(,)?)+)' \
           '(\s)(налогов)(ый|ого|ым|ому|ом)(\s)(кодекс)(а|у|е|ом)+'
pattern3 = '(\b)(((\s)[0-9]{1,5}(,)?)+)(\s)(гк)(\b)'
pattern4 = '(\b)(((\s)[0-9]{1,5}(,)?)+)(\s)(нк)(\b)'


def counter(text, codex):
    global countGK
    global obshiycountGK
    global countNK
    global obshiycountNK

    for s in range(len(text)):
        a = list(text[s])
        b = ''.join(a)
        # print(b)
        if codex == 'гк':
            countGK += (len([int(l) for l in b.split() if l.isdigit()]) - 1)
            arrGK.append(countGK)
        elif codex == 'нк':
            countNK += (len([int(l) for l in b.split() if l.isdigit()]) - 1)
            arrNK.append(countNK)
    obshiycountGK += countGK
    obshiycountNK += countNK


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


def parse(filename):
    global obshiycountGK
    obshiycountGK = 0
    global obshiycountNK
    obshiycountNK = 0

    with open('./media/' + filename, encoding='cp1251') as file:
        contents = file.read()
    contents = contents.lower().replace(',', '')
    for solution in contents.split('------------------------------------------------------------------'):
        if solution.find('установил:') == -1 or solution.find('постановил:') == -1:
            continue
        solution_parse = solution.split('установил:')[1]
        solution_parse = solution_parse.split('постановил:')[0]
        analyze(solution_parse)
    return (obshiycountNK, obshiycountGK)

#parse('documents/2018/08/14/1_АС_897_решений_за_июль_2016_dsBofKz.txt')

print(obshiycountGK)
print(obshiycountNK)
print(arrGK)
print(arrNK)