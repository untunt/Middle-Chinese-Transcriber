# unt's Ancient (Middle) Chinese Phonology Transcriber
# unt 的中古音韵转写器

import sys
from lists import *

# Convert varient characters (异体字) to its index (row no.)
# simplified character is in column 'zimu'
# varient characters are in column '_vari'
# the parameter in_type is just a syntactic sugar
def vari2index(in_str, in_type, list_name):
    index = [list_name['_vari'].index(vari) for vari in list_name['_vari'] if in_str in vari]
    if len(index) == 0:
        return -1
    return index[0]

def str2index(in_str, in_type, list_name):
    if not in_str in list_name[in_type]:
        if in_type == 'zimu':
            return vari2index(in_str, in_type, list_name)
        else:
            return -1
    return list_name[in_type].index(in_str)

def index2str(index, out_type, list_name):
    if index < 0:
        return index
    return list_name[out_type][index]

# Return the Voicing (清浊) of given onset index
def qzh(index):
    if onset['_qzh'][index] == '全清':
        return 1;
    if onset['_qzh'][index] == '次清':
        return 2;
    if onset['_qzh'][index] == '全浊':
        return 3;
    return 4; # '次浊'

def convert(in_str, in_type, out_type):
    # analyze input
    if in_type == 'zimu':
        # index of onset
        onset_i = str2index(in_str[0], in_type, onset)
        if onset_i < 0:
            print('Error: The onset \"' + in_str + '\" cannot be found in the list! (code: ' + str(onset_i) + ')')

        # rhyme part
        r = in_str[1:]

        # get and remove tone (调/diao)
        if '平' in r: # 1st tone (平声/pingsheng) appears most
            tone = 1
        elif '入' in r: # 4th tone (入声/rusheng)
            tone = 4
        elif '去' in r: # 3rd tone (去声/qusheng)
            tone = 3
        elif '上' in r: # 2nd tone (上声/shangsheng)
            tone = 2
        else:
            print('Error: The descrption \"' + in_str + '\" contains no tone! 1st tone (平声) is set.')
            tone = 1
        r = r.strip('平上赏賞去入声聲调調')

        # index of rhyme
        rhyme_i = str2index(r, in_type, rhyme)
        # complex rhyme search needed occasion
    
    # generate output
    #print(index2str(rhyme_i, out_type, rhyme))
    out_str = index2str(onset_i, out_type, onset) + index2str(rhyme_i, out_type, rhyme)
    if out_type == 'unt':
        if tone == 1: # 平声
            if qzh(onset_i) < 3:
                out_str += '˦˦'
            else:
                out_str += '˨˨'
        elif tone == 4: # 入声
            if out_str[-2:] == 'ŋ':
                out_str = out_str[0:-2] + 'k'
            elif out_str[-1] == 'n':
                out_str = out_str[0:-1] + 't'
            elif out_str[-1] == 'm':
                out_str = out_str[0:-1] + 'p'
            #else:
            #    print('Error')
            if qzh(onset_i) < 3:
                out_str += '˥˧'
            else:
                out_str += '˧˩'
        elif tone == 3: # 去声
            if qzh(onset_i) < 3:
                out_str += '˥˧'
            else:
                out_str += '˧˩'
        else: # tone == 2; 上声
            if qzh(onset_i) < 3:
                out_str += '˧˥'
            else:
                out_str += '˩˧'
    elif out_type == 'poly':
        if tone != 1:
            if tone == 4: # 入声
                if out_str[-2:] == 'ng':
                    out_str = out_str[0:-2] + 'k'
                elif out_str[-1] == 'n':
                    out_str = out_str[0:-1] + 't'
                elif out_str[-1] == 'm':
                    out_str = out_str[0:-1] + 'p'
                #else:
                #    print('Error')
            elif tone == 3: # 去声
                if out_str[-1] != 'd':
                    out_str += 'h'
            else: # tone == 2; 上声
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

word = in_str.split()
for i, s in enumerate(word):
    word[i] = convert(s, in_type, out_type);
out_str = ' '.join(word)

print()
print('====================================')
print('|  unt\'s Ancient (Middle) Chinese  |')
print('|      Phonology  Transcriber      |')
print('|      (unt 的中古音韵转写器)      |')
print('====================================')
print()
print(out_str)
print()
