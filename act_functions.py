def replace_in_head(string, old, new, head_len):
    return string[:head_len].replace(old, new) + string[head_len:]


def read_file(file_name):
    result = {}
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        lines = [line.rstrip(',').split(',') for line in f.readlines()]
        for index, head in enumerate(lines[0]):
            result[head] = [line[index] for line in lines[1:]]
    return result


# 声母
onset = read_file('list_initials.csv')
# 韵母
rhyme = read_file('list_finals.csv')
# IPA tone letters
# order: 阴平, 阳平, 阴上, 阳上, 阴去, 阳去, 阴入, 阳入
tone_letters = {
    'unt': ['˦', '˨˩', '˦˦˥', '˨˨˧', '˥˩', '˧˩˨', '˥', '˨˩'],
    'untF': ['˦', '˨', '˧˥', '˩˧', '˥˧', '˧˩', '˥˧', '˧˩']
}


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
    if out_type == 'bax1':
        return list_name['bax'][index]
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
        # INITIALS
        # for division I, replace 见 series initials with uvulars
        if out_type == 'unt' and rhyme['_deng'][rhyme_index] == '一':
            initials_from = 'kɡŋhɦ'
            initials_to = 'qɢɴχʁ'
            i = initials_from.find(out_str[0])
            if i >= 0:
                out_str = replace_in_head(out_str, initials_from[i], initials_to[i], 1)

        # FINALS
        # set 蒸 rhyme to division III type A after 精 and 章 groups initials
        if rhyme['_yun'][rhyme_index] == '蒸' and \
                (onset['_zu'][onset_index] in '精章' or onset['zimu'][onset_index] in '以日'):
            out_str = out_str.replace('ɻ', '')
        # set 谆 and 清 rhyme to division III type B after 知 and 庄 groups initials
        if rhyme['_yun'][rhyme_index] in '谆清' and onset['_zu'][onset_index] in '知庄':
            out_str = out_str.replace('j', 'ɻj')
            out_str = out_str.replace('ɥ', 'ɻɥ')
        # remove [ᵊ] in 侯 rhyme after 帮 group initials
        if onset['_zu'][onset_index] == '帮':
            out_str = out_str.replace('ᵊ', '')

        # MEDIALS
        # modify medials after 帮 group initials
        if onset['_zu'][onset_index] == '帮':
            # 2019 version:
            if 'ɥ̈' not in out_str:
                out_str = replace_in_head(out_str, 'ɥ', 'j', 2)
            out_str = replace_in_head(out_str, 'ẅ', 'ɥ̈', 3)
            out_str = replace_in_head(out_str, 'j̈', 'ɥ̈', 3)
            if out_str[1] == 'ɨ':
                out_str = replace_in_head(out_str, 'ɨ', 'ɥ̈ɨ', 2)
            out_str = replace_in_head(out_str, 'w', '', 2)
            # 2016 version:
            out_str = replace_in_head(out_str, 'u̯', '', 3)
        # for division II, write the medial as [ɻw] after 知 and 庄 groups initials
        if rhyme['_deng'][rhyme_index] == '二' and onset['_zu'][onset_index] in '知庄':
            out_str = out_str.replace('wɻ', 'ɻw')
        # remove redundant [j] (以 initial)
        if ('jj̈' not in out_str) and ('jɥ̈' not in out_str):
            out_str = out_str.replace('jj', 'j')
            out_str = out_str.replace('jɥ', 'ɥ')
        # add [j̈] (云 initial) before [ɨ] (and [i], only 真 rhyme)
        if out_str[0] in 'ɨi':
            out_str = 'j̈' + out_str

        # TONES
        # for tone 4, replace nasal codas with stops
        if tone == 4:
            if out_str[-2:] == 'ŋʷ':
                out_str = out_str[0:-2] + 'kʷ'
            else:
                codas_from = 'mnɲŋ'
                codas_to = 'ptck'
                i = codas_from.find(out_str[-1])
                if i >= 0:
                    out_str = out_str[0:-1] + codas_to[i]
                else:
                    error_fourth_tone(word)
        # add tone letters
        tone_letter_index = (tone - 1) * 2
        # use dark (阳) tone for 浊平, 全浊上, 浊去, and 全浊入
        if ((tone == 1 or tone == 3) and qzh(onset_index) >= 3) or \
                ((tone == 2 or tone == 4) and qzh(onset_index) == 3):
            tone_letter_index += 1
        out_str += tone_letters[out_type][tone_letter_index]
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
    elif out_type == 'bax' or out_type == 'bax1':
        # After labial initials, there is no contrast between -an, -at, -a and -wan, -wat, -wa
        if onset['_zu'][onset_index] == '帮' and rhyme['_yun'][rhyme_index] in '废桓戈阳':
            out_str = out_str.replace('w', '')

        # [chongniu] is limited to syllables with grave initials
        if onset['_zu'][onset_index] not in '帮见影' \
                and ('c' in rhyme['_overlap'][rhyme_index] or rhyme['_yun'][rhyme_index] == '清'):
            if rhyme['_yun'][rhyme_index] in '脂真諄侵':
                out_str = out_str.replace('ji', 'i')
                out_str = out_str.replace('jwi', 'wi')
            else:
                out_str = out_str.replace('ji', 'j')
                out_str = out_str.replace('jwi', 'jw')
        # a prevocalic -j- in the final is omitted after Tsy-
        if 'y' in out_str:
            out_str = out_str.replace('yj', 'y')
            out_str = out_str.replace('yhj', 'yh')

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
                out_str += 'H'
            else:  # tone == 2; 上声
                out_str += 'X'
        if out_type == 'bax1':
            out_str = out_str.replace('\'', 'ʔ')
            if rhyme['_yun'][rhyme_index] == '佳':
                out_str = out_str.replace('ea', 'ɛɨ')
            out_str = out_str.replace('+', 'ɨ')
            out_str = out_str.replace('ae', 'æ')
            out_str = out_str.replace('ea', 'ɛ')
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
