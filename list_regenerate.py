# regenerate consonants and vowels list from list_consonant.txt

def writelist(file, english_name, chinese_name):
    with open('list_' + english_name + '.txt', encoding='utf_16') as fi:
        lines = fi.readlines()

    data = []
    for line in lines:
        data.append(line.replace('\n', '').split('\t'))
        
    f.write('# ' + chinese_name + '\n')
    f.write(english_name + ' = {\n')
    for j in range(1, len(data[0])):
        if j != 1:
            f.write(',\n')
        f.write('    \'' + data[0][j] + '\': [')
        
        for i in range(1, len(data)):
            if i != 1:
                f.write(',')
            if data[i][0] == '1':
                f.write('\n       ')
            f.write(' \'' + data[i][j] + '\'')
            
        f.write('\n    ]')
    f.write('\n}\n\n')


f = open('list.py', 'w', encoding='utf_8')
writelist(f, 'consonant', '声母')
f.close()
