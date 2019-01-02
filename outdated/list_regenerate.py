# regenerate consonants and vowels list from list_consonant.txt


def write_list(file, english_name, chinese_name):
    with open('list_' + english_name + '.txt', encoding='utf_16') as fi:
        lines = fi.readlines()

    data = []
    for line in lines:
        data.append(line.replace('\n', '').split('\t'))
        
    file.write('# ' + chinese_name + '\n')
    file.write(english_name + ' = {\n')
    for j in range(1, len(data[0])):
        if j != 1:
            file.write(',\n')
        file.write('    \'' + data[0][j] + '\': [')
        
        for i in range(1, len(data)):
            if i != 1:
                file.write(',')
            if data[i][0] == '1':
                file.write('\n       ')
            file.write(' \'' + data[i][j] + '\'')
            
        file.write('\n    ]')
    file.write('\n}\n\n')


f = open('lists.py', 'w', encoding='utf_8')
write_list(f, 'onset', '声母')
write_list(f, 'rhyme', '韵母')
f.close()
