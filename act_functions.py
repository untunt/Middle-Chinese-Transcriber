def read_csv(file_name):
    result = {}
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        lines = [line.rstrip(',').split(',') for line in f.readlines()]
        for index, head in enumerate(lines[0]):
            result[head] = [line[index] for line in lines[1:]]
    return result


# 声母
initials = read_csv('list_initials.csv')
# 韵母
finals = read_csv('list_finals.csv')
# IPA tone letters
# order: 阴平, 阳平, 阴上, 阳上, 阴去, 阳去, 阴入, 阳入
tone_letters = {
    'unt': ['˦', '˨˩', '˦˦˥', '˨˨˧', '˥˩', '˧˩˨', '˥', '˨˩'],
    'untF': ['˦', '˨', '˧˥', '˩˧', '˥˧', '˧˩', '˥˧', '˧˩']
}


# Error Messages
ERROR_INITIAL_NOT_FOUND = 'The initial of "{}" cannot be found in the list!'
ERROR_FINAL_NOT_FOUND = 'The final of "{}" cannot be found in the list!'
ERROR_TONE_NOT_FOUND = 'The description "{}" contains no tone! Tone 1 (平声) is set.'
ERROR_TONE_4 = 'The rhyme of "{}" is not a tone-4 rhyme but it has tone 4!'


def error(error_type, *args):
    print('Error: ' + error_type.format(*args))


def replace_in_head(string, old, new, head_len):
    return string[:head_len].replace(old, new) + string[head_len:]


# Convert variant characters (异体字) to its index (row no.)
# simplified character is in column 'trad'
# variant characters are in column '_var'
def vari2index(in_str, list_name):
    index = [list_name['_var'].index(var) for var in list_name['_var'] if in_str in var]
    if len(index) == 0:
        return -1
    return index[0]


def str2index(in_str, in_type, list_name):
    if in_str in list_name[in_type]:
        return list_name[in_type].index(in_str)

    # if not, the input string may be a variant trad or a complex trad
    if in_type == 'trad':
        if list_name == initials:
            return vari2index(in_str, list_name)

        # for rhyme, get and remove division (等) and rounding (呼)
        division = ''
        chongniu = ''
        rounding = ''
        # division I, II, III, and IV
        for div in '一二三四':
            if div in in_str:
                division = div
                break
        # division III type A or B
        if 'A' in in_str or 'a' in in_str:
            chongniu = 'A'
        elif 'B' in in_str or 'b' in in_str:
            chongniu = 'B'
        # open mouth (开口) or closed mouth (合口)
        if '开' in in_str or '開' in in_str:
            rounding = '开'
        elif '合' in in_str:
            rounding = '合'
        in_str = in_str.strip('一二三四AaBb开開合口')

        if len(in_str) != 1:
            return -1
        if in_str in list_name['_rhyme']:
            first_index = list_name['_rhyme'].index(in_str)
        else:
            first_index = vari2index(in_str, list_name)
        if first_index == -1 or list_name['_multi'][first_index] == '':
            return first_index

        # 真 rhyme rounded has only type B
        if list_name['_rhyme'][first_index] == '真' and rounding == '合' and chongniu == '':
            chongniu = 'B'

        iter_index = first_index
        while list_name['_rhyme'][iter_index] == list_name['_rhyme'][first_index]:
            found = True
            if 'd' in list_name['_multi'][iter_index] and \
                    (division == '' or division not in list_name['_div'][iter_index]):
                found = False
            # if chongniu == '', type A is set as default (except for 真 rhyme rounded)
            if 'c' in list_name['_multi'][iter_index] and chongniu not in list_name['_div'][iter_index]:
                found = False
            if 'r' in list_name['_multi'][iter_index] and rounding != list_name['_round'][iter_index]:
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


# Return the voicing (清浊) of given initial index
def get_voicing(index):
    return 1 + ['全清', '次清', '全浊', '次浊'].index(initials['_voice'][index])


# Convert nasal coda to stop coda
def coda_nasal2stop(rhyme, word):
    if rhyme[-2:] == 'ng':
        rhyme = rhyme[0:-2] + 'k'
    elif rhyme[-2:] == 'ŋʷ':
        rhyme = rhyme[0:-2] + 'kʷ'
    else:
        codas_from = 'mnɲŋ'
        codas_to = 'ptck'
        i = codas_from.find(rhyme[-1])
        if i >= 0:
            rhyme = rhyme[0:-1] + codas_to[i]
        else:
            error(ERROR_TONE_4, word)
    return rhyme


def convert_input(word, in_type):
    # analyze the input string and split it into 3 parts: initial, final and tone
    in_onset = ''
    in_rhyme = ''
    tone = 0
    if in_type == 'trad':
        in_onset = word[0]
        in_rhyme = word[1:]
        # get and remove the tone (调)
        tones = '平上去入'
        for i in range(len(tones)):
            if tones[i] in in_rhyme:
                tone = i + 1
                break
        in_rhyme = in_rhyme.strip('平上赏賞去入声聲调調')
    onset_index = str2index(in_onset, in_type, initials)
    if onset_index < 0:
        error(ERROR_INITIAL_NOT_FOUND, word)
    rhyme_index = str2index(in_rhyme, in_type, finals)
    if rhyme_index < 0:
        error(ERROR_FINAL_NOT_FOUND, word)
    if tone == 0:
        error(ERROR_TONE_NOT_FOUND, word)
        tone = 1
    # complex final search needed occasion

    return onset_index, rhyme_index, tone


def convert_output(onset_index, rhyme_index, tone, out_type, word):
    out_onset = index2str(onset_index, out_type, initials)
    out_rhyme = index2str(rhyme_index, out_type, finals)
    out_str = out_onset + out_rhyme
    if out_type == 'unt' or out_type == 'untF':
        # INITIALS
        # for division non-III, replace 见 series initials with uvulars
        if out_type == 'unt' and finals['_div'][rhyme_index] != '三':
            initials_from = 'kɡŋhɦ'
            initials_to = 'qɢɴχʁ'
            i = initials_from.find(out_str[0])
            if i >= 0:
                out_str = replace_in_head(out_str, initials_from[i], initials_to[i], 1)

        # FINALS
        # set 蒸 rhyme to division III type A after 精 and 章 groups initials
        if finals['_rhyme'][rhyme_index] == '蒸' and \
                (initials['_group'][onset_index] in '精章' or initials['trad'][onset_index] in '以日'):
            out_str = out_str.replace('ɻ', '')
        # set 谆 and 清 rhyme to division III type B after 知 and 庄 groups initials
        if finals['_rhyme'][rhyme_index] in '谆清' and initials['_group'][onset_index] in '知庄':
            out_str = out_str.replace('j', 'ɻj')
            out_str = out_str.replace('ɥ', 'ɻɥ')

        # MEDIALS
        # modify medials after 帮 group initials
        if initials['_group'][onset_index] == '帮':
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
        if finals['_div'][rhyme_index] == '二' and initials['_group'][onset_index] in '知庄':
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
            out_str = coda_nasal2stop(out_str, word)
        # add tone letters
        tone_letter_index = (tone - 1) * 2
        # use dark (阳) tone for 浊平, 全浊上, 浊去, and 全浊入
        if ((tone == 1 or tone == 3) and get_voicing(onset_index) >= 3) or \
                ((tone == 2 or tone == 4) and get_voicing(onset_index) == 3):
            tone_letter_index += 1
        out_str += tone_letters[out_type][tone_letter_index]
    elif out_type == 'poly':
        # 1. 含r之声母（知组与庄组）及二等韵（以r起始）相拼时省去一r
        out_str = out_str.replace('rr', 'r')

        # 2. 唇牙喉音声母之重纽A类（即重纽四等，含谆韵）于声、韵母间加一j
        if ('A' in finals['trad'][rhyme_index] or finals['trad'][rhyme_index] == '臻') \
                and (initials['_group'][onset_index] in ['帮', '见'] or out_onset in ['h', 'qh']):
            out_str = out_onset + 'j' + out_rhyme

        # 3. j与开口三等韵相拼时，除脂ii、之i、真in、蒸ing、侵im五韵外，j后面之i应省去
        if finals['_rhyme'][rhyme_index] not in ['脂', '之', '真', '蒸', '侵']:
            out_str = out_str.replace('ji', 'j')

        # 5. 若声母与韵母搭配不正常（一般为三等与非三等搭配问题），可以'分隔声韵母
        if initials['_group'][onset_index] in ['章', '以', '日'] and out_rhyme[0] not in ['i', 'y', 'j']:
            out_str = out_onset + "'" + out_rhyme

        # convert tone
        if tone == 2:
            out_str += 'x'
        elif tone == 3:
            if out_str[-1] != 'd':
                out_str += 'h'
        elif tone == 4:
            out_str = coda_nasal2stop(out_str, word)
    elif out_type == 'bax' or out_type == 'bax1':
        # after 帮 group, there is no contrast between -an, -at, -a and -wan, -wat, -wa
        # and generally remove 'w' after 帮 group when the rhyme has both rounded and unrounded finals
        if initials['_group'][onset_index] == '帮' and (finals['_rhyme'][rhyme_index] in '废桓戈阳' or
                                                       'r' in finals['_multi'][rhyme_index]):
            out_str = out_str.replace('w', '')

        # [chongniu] is limited to syllables with grave initials
        if (initials['_group'][onset_index] not in '帮见影' or initials['trad'][onset_index] == '云') \
                and ('c' in finals['_multi'][rhyme_index] or finals['_rhyme'][rhyme_index] in '谆清'):
            if finals['_rhyme'][rhyme_index] in '脂真谆侵':
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
        if tone == 2:
            out_str += 'X'
        elif tone == 3:
            out_str += 'H'
        elif tone == 4:
            out_str = coda_nasal2stop(out_str, word)

        if out_type == 'bax1':
            out_str = out_str.replace('\'', 'ʔ')
            if finals['_rhyme'][rhyme_index] == '佳':
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
