# unt’s Ancient (Middle) Chinese Phonology Transcriber
# unt 的中古音韵转写器

import sys
from lists import *


# Convert variant characters (异体字) to its index (row no.)
# simplified character is in column 'zimu'
# variant characters are in column '_vari'
# the parameter in_type is just a syntactic sugar
def variant_to_index(in_string, in_type, list_name):
    index = [list_name['_vari'].index(vari) for vari in list_name['_vari'] if in_string in vari]
    if len(index) == 0:
        return -1
    return index[0]


def str2index(in_string, in_type, list_name):
    if in_string not in list_name[in_type]:
        if in_type == 'zimu':
            if list_name == onset:
                return variant_to_index(in_string, in_type, list_name)

            # for rhyme
            # get and remove deng-hu (等呼)
            deng = ''
            chongniu = ''
            hu = ''
            if '一' in in_string:  # 1st deng
                deng = '一'
            elif '二' in in_string:  # 2nd deng
                deng = '二'
            elif '三' in in_string:  # 3rd deng
                deng = '三'
                if 'A' in in_string or 'a' in in_string:  # 3a deng
                    chongniu = 'A'
                elif 'B' in in_string or 'b' in in_string:  # 3b deng
                    chongniu = 'B'
            elif '四' in in_string:  # 4th deng
                deng = '四'
            if '开' in in_string or '開' in in_string:  # unrounded (开口)
                hu = '开'
            elif '合' in in_string:  # rounded (合口)
                hu = '合'
            in_string = in_string.strip('一二三四AaBb开開合口')

            if len(in_string) != 1:
                return -1
            if in_string in list_name['_yun']:
                first_i = list_name['_yun'].index(in_string)
            else:
                first_i = variant_to_index(in_string, in_type, list_name)
            if first_i == -1 or list_name['_overlap'][first_i] == '':
                return first_i

            iter_i = first_i
            while list_name['_yun'][iter_i] == list_name['_yun'][first_i]:
                found = True
                if 'd' in list_name['_overlap'][iter_i] and deng not in list_name['_deng'][iter_i]:
                    found = False
                if 'c' in list_name['_overlap'][iter_i] and chongniu not in list_name['_deng'][iter_i]:
                    found = False
                if 'h' in list_name['_overlap'][iter_i] and hu != list_name['_hu'][iter_i]:
                    found = False
                if found:
                    return iter_i
                iter_i += 1
            return -1
        else:
            return -1
    return list_name[in_type].index(in_string)


def index2str(index, out_type, list_name):
    if index < 0:
        return index
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


def convert(in_str, in_type, out_type):
    # analyze input
    if in_type == 'zimu':
        # index of onset
        onset_i = str2index(in_str[0], in_type, onset)
        if onset_i < 0:
            print('Error: The onset \"' + in_str[0] + '\" cannot be found in the list! (code: ' + str(onset_i) + ')\n')
            return 'Error'

        # rhyme part
        r = in_str[1:]

        # get and remove tone (调/diao)
        if '平' in r:  # 1st tone (平声/pingsheng) appears most
            tone = 1
        elif '入' in r:  # 4th tone (入声/rusheng)
            tone = 4
        elif '去' in r:  # 3rd tone (去声/qusheng)
            tone = 3
        elif '上' in r:  # 2nd tone (上声/shangsheng)
            tone = 2
        else:
            print('Error: The description \"' + in_str + '\" contains no tone! 1st tone (平声) is set.\n')
            tone = 1
        r = r.strip('平上赏賞去入声聲调調')

        # index of rhyme
        rhyme_i = str2index(r, in_type, rhyme)
        if rhyme_i < 0:
            print('Error: The rhyme \"' + in_str + '\" cannot be found in the list! (code: ' + str(rhyme_i) + ')\n')
            return 'Error'
        # complex rhyme search needed occasion

    # generate output
    # print(index2str(rhyme_i, out_type, rhyme))
    out_onset = index2str(onset_i, out_type, onset)
    out_rhyme = index2str(rhyme_i, out_type, rhyme)
    out_str = out_onset + out_rhyme
    if out_type == 'unt':
        if tone == 1:  # 平声
            if qzh(onset_i) < 3:
                out_str += '˦˦'
            else:
                out_str += '˨˨'
        elif tone == 4:  # 入声
            if out_str[-1] == 'ŋ':
                out_str = out_str[0:-1] + 'k'
            elif out_str[-1] == 'n':
                out_str = out_str[0:-1] + 't'
            elif out_str[-1] == 'm':
                out_str = out_str[0:-1] + 'p'
            else:
                print('Error: The rhyme of \"' + in_str + '\" is not a 4th-tone rhyme but its tone is 4th!\n')
            if qzh(onset_i) < 3:
                out_str += '˥˧'
            else:
                out_str += '˧˩'
        elif tone == 3:  # 去声
            if qzh(onset_i) < 3:
                out_str += '˥˧'
            else:
                out_str += '˧˩'
        else:  # tone == 2; 上声
            if qzh(onset_i) < 3:
                out_str += '˧˥'
            else:
                out_str += '˩˧'
        if onset['_zu'][onset_i] == '帮':  # remove medial "u" after bilabial consonant
            out_str = out_str.replace('u̯', '')
    elif out_type == 'poly':
        # 1. 含r之声母（知组与庄组）及二等韵（以r起始）相拼时省去一r
        out_str = out_str.replace('rr', 'r')

        # 2. 唇牙喉音声母之重纽A类（即重纽四等，含谆韵）于声、韵母间加一j
        if ('A' in rhyme['zimu'][rhyme_i] or rhyme['zimu'][rhyme_i] == '臻') \
                and (onset['_zu'][onset_i] in ['帮', '见'] or out_onset in ['h', 'qh']):
            out_str = out_onset + 'j' + out_rhyme

        # 3. j与开口三等韵相拼时，除脂ii、之i、真in、蒸ing、侵im五韵外，j后面之i应省去
        if rhyme['_yun'][rhyme_i] not in ['脂', '之', '真', '蒸', '侵']:
            out_str = out_str.replace('ji', 'j')

        # 5. 若声母与韵母搭配不正常（一般为三等与非三等搭配问题），可以'分隔声韵母
        if onset['_zu'][onset_i] in ['章', '以', '日'] and out_rhyme[0] not in ['i', 'y', 'j']:
            out_str = out_onset + '\'' + out_rhyme

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


argc = len(sys.argv)
if argc > 3:
    in_type = sys.argv[3]
else:
    in_type = 'zimu'
if argc > 2:
    out_type = sys.argv[2]
else:
    out_type = 'unt'
in_str = sys.argv[1]

print()
print('====================================')
print('|  unt\'s Ancient (Middle) Chinese  |')
print('|      Phonology  Transcriber      |')
print('|      (unt 的中古音韵转写器)      |')
print('====================================')
print()

word = in_str.split()
for i, s in enumerate(word):
    word[i] = convert(s, in_type, out_type);
out_str = ' '.join(word)

print(out_str)
print()
