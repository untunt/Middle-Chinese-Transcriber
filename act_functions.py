def read_file(file_name):
    result = {}
    with open(file_name, 'r', encoding='utf_16') as f:
        lines = [line.rstrip('\n').split('\t') for line in f.readlines()]
        for index, head in enumerate(lines[0]):
            result[head] = [line[index] for line in lines[1:]]
    return result


# 声母
onset = read_file('list_onset.txt')
# 韵母
rhyme = read_file('list_rhyme.txt')


# Convert variant characters (异体字) to its index (row no.)
# simplified character is in column 'zimu'
# variant characters are in column '_vari'
# the parameter in_type is just a syntactic sugar
def vari2index(in_str, list_name):
    index = [list_name['_vari'].index(vari) for vari in list_name['_vari'] if in_str in vari]
    if len(index) == 0:
        return -1
    return index[0]


def str2index(in_str, in_type, list_name):
    if in_str in list_name[in_type]:
        return list_name[in_type].index(in_str)

    # if not, the input string may be a variant zimu or a complex zimu
    if in_type == 'zimu':
        if list_name == onset:
            return vari2index(in_str, list_name)

        # for rhyme
        # get and remove deng-hu (等呼)
        deng = ''
        chongniu = ''
        hu = ''
        if '一' in in_str:  # 1st deng
            deng = '一'
        elif '二' in in_str:  # 2nd deng
            deng = '二'
        elif '三' in in_str:  # 3rd deng
            deng = '三'
            if 'A' in in_str or 'a' in in_str:  # 3a deng
                chongniu = 'A'
            elif 'B' in in_str or 'b' in in_str:  # 3b deng
                chongniu = 'B'
        elif '四' in in_str:  # 4th deng
            deng = '四'
        if '开' in in_str or '開' in in_str:  # unrounded (开口)
            hu = '开'
        elif '合' in in_str:  # rounded (合口)
            hu = '合'
        in_str = in_str.strip('一二三四AaBb开開合口')

        if len(in_str) != 1:
            return -1
        if in_str in list_name['_yun']:
            first_index = list_name['_yun'].index(in_str)
        else:
            first_index = vari2index(in_str, list_name)
        if first_index == -1 or list_name['_overlap'][first_index] == '':
            return first_index

        iter_index = first_index
        while list_name['_yun'][iter_index] == list_name['_yun'][first_index]:
            found = True
            if 'd' in list_name['_overlap'][iter_index] and deng not in list_name['_deng'][iter_index]:
                found = False
            if 'c' in list_name['_overlap'][iter_index] and chongniu not in list_name['_deng'][iter_index]:
                found = False
            if 'h' in list_name['_overlap'][iter_index] and hu != list_name['_hu'][iter_index]:
                found = False
            if found:
                return iter_index
            iter_index += 1
        return -1
    return -1


def index2str(index, out_type, list_name):
    if index < 0:
        return ''
    return list_name[out_type][index]


# Return the voicing (清浊/qingzhuo) of given onset index
def qzh(index):
    if onset['_qzh'][index] == '全清':
        return 1
    if onset['_qzh'][index] == '次清':
        return 2
    if onset['_qzh'][index] == '全浊':
        return 3
    return 4  # '次浊'


def error(message):
    print('Error: ' + message)


def error_fourth_tone(word):
    error('The rhyme of "' + word + '" is not a 4th-tone rhyme but its tone is the 4th!')


def convert_input(word, in_type):
    # analyze the input string and split it into 3 parts: onset, rhyme and tone
    in_onset = ''
    in_rhyme = ''
    tone = 0
    if in_type == 'zimu':
        in_onset = word[0]
        in_rhyme = word[1:]
        # get and remove the tone (调/diao)
        if '平' in in_rhyme:  # 1st tone (平声/pingsheng) appears most
            tone = 1
        elif '入' in in_rhyme:  # 4th tone (入声/rusheng)
            tone = 4
        elif '去' in in_rhyme:  # 3rd tone (去声/qusheng)
            tone = 3
        elif '上' in in_rhyme:  # 2nd tone (上声/shangsheng)
            tone = 2
        in_rhyme = in_rhyme.strip('平上赏賞去入声聲调調')
    onset_index = str2index(in_onset, in_type, onset)
    if onset_index < 0:
        error('The onset "' + word[0] + '" cannot be found in the list! (code: ' + str(onset_index) + ')')
    rhyme_index = str2index(in_rhyme, in_type, rhyme)
    if rhyme_index < 0:
        error('The rhyme "' + in_rhyme + '" cannot be found in the list! (code: ' + str(rhyme_index) + ')')
    if tone == 0:
        error('The description "' + word + '" contains no tone! 1st tone (平声) is set.')
        tone = 1
    # complex rhyme search needed occasion

    return onset_index, rhyme_index, tone


def convert_output(onset_index, rhyme_index, tone, out_type, word):
    out_onset = index2str(onset_index, out_type, onset)
    out_rhyme = index2str(rhyme_index, out_type, rhyme)
    out_str = out_onset + out_rhyme
    if out_type == 'unt' or out_type == 'untF':
        if tone == 1:  # 平声
            if qzh(onset_index) < 3:
                out_str += '˦'
            else:
                out_str += '˨'
        elif tone == 4:  # 入声
            if out_str[-2:] == 'ŋʷ':
                out_str = out_str[0:-2] + 'kʷ'
            elif out_str[-1] == 'ŋ':
                out_str = out_str[0:-1] + 'k'
            elif out_str[-1] == 'ɲ':
                out_str = out_str[0:-1] + 'c'
            elif out_str[-1] == 'n':
                out_str = out_str[0:-1] + 't'
            elif out_str[-1] == 'm':
                out_str = out_str[0:-1] + 'p'
            else:
                error_fourth_tone(word)
            if qzh(onset_index) < 3:
                out_str += '˥˧'
            else:
                out_str += '˧˩'
        elif tone == 3:  # 去声
            if qzh(onset_index) < 3:
                out_str += '˥˧'
            else:
                out_str += '˧˩'
        else:  # tone == 2; 上声
            if qzh(onset_index) < 3:
                out_str += '˧˥'
            else:
                out_str += '˩˧'
        if onset['_zu'][onset_index] == '帮':  # remove medial "u" after bilabial consonant
            def replace_medial(string, old, new, end=2):
                return string[:end].replace(old, new) + string[end:]
            out_str = replace_medial(out_str, 'w', '')
            out_str = replace_medial(out_str, 'ɥ', 'j')
            out_str = replace_medial(out_str, 'u̯', '', 3)
    elif out_type == 'poly':
        # 1. 含r之声母（知组与庄组）及二等韵（以r起始）相拼时省去一r
        out_str = out_str.replace('rr', 'r')

        # 2. 唇牙喉音声母之重纽A类（即重纽四等，含谆韵）于声、韵母间加一j
        if ('A' in rhyme['zimu'][rhyme_index] or rhyme['zimu'][rhyme_index] == '臻') \
                and (onset['_zu'][onset_index] in ['帮', '见'] or out_onset in ['h', 'qh']):
            out_str = out_onset + 'j' + out_rhyme

        # 3. j与开口三等韵相拼时，除脂ii、之i、真in、蒸ing、侵im五韵外，j后面之i应省去
        if rhyme['_yun'][rhyme_index] not in ['脂', '之', '真', '蒸', '侵']:
            out_str = out_str.replace('ji', 'j')

        # 5. 若声母与韵母搭配不正常（一般为三等与非三等搭配问题），可以'分隔声韵母
        if onset['_zu'][onset_index] in ['章', '以', '日'] and out_rhyme[0] not in ['i', 'y', 'j']:
            out_str = out_onset + "'" + out_rhyme

        # convert tone
        if tone != 1:
            if tone == 4:  # 入声
                if out_str[-2:] == 'ng':
                    out_str = out_str[0:-2] + 'k'
                elif out_str[-1] == 'n':
                    out_str = out_str[0:-1] + 't'
                elif out_str[-1] == 'm':
                    out_str = out_str[0:-1] + 'p'
                # else:
                #    print('Error')
            elif tone == 3:  # 去声
                if out_str[-1] != 'd':
                    out_str += 'h'
            else:  # tone == 2; 上声
                out_str += 'x'
    return out_str


def act(words_str, in_type, out_type):
    words = words_str.split()
    for i, word in enumerate(words):
        (onset_index, rhyme_index, tone) = convert_input(word, in_type)
        words[i] = convert_output(onset_index, rhyme_index, tone, out_type, word)
    if '\t' in words_str:
        return '\t'.join(words)
    return ' '.join(words)


def print_logo():
    print("""
=========================
  unt' s Middle Chinese
  Phonology Transcriber

   unt 的中古音韵转写器
=========================
""")
