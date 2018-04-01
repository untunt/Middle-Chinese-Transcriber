import sys
from list import *

def convert_core(in_str, in_type, out_type, list_name):
    if in_str not in list_name[in_type] and in_type == 'zimu':
        index = list_name['vari'].index(in_str)
    else:
        index = list_name[in_type].index(in_str)
    return list_name[out_type][index]

def convert(in_str, in_type, out_type, list_name):
    if in_type == 'zimu':
        c = convert_core(s[0], in_type, out_type, list_name)
        v = s[1:]

        # get and remove tone (调/diao)
        if '平' in v: # 1st tone (平声) appears most
            diao = 1
        elif '入' in v:
            diao = 4
        elif '去' in v:
            diao = 3
        else:
            diao = 2    
        v = v.strip('平上赏賞去入声聲调調')
        return (onset, rhyme, tone)

# 
def str2index(in_str, in_type, list_name):
        
    return (onset, rhyme, tone)



argc = len(sys.argv)
if argc > 3:
    out_type = sys.argv[3]
else:
    out_type = 'poly' # 'ipa_u'
if argc > 2:
    in_type = sys.argv[2]
else:
    in_type = 'zimu'
in_str = sys.argv[1]

word = in_str.split()
for i, s in enumerate(word):
    word[i] = convert(s, in_type, out_type, list_name);
out_str = ' '.join(word)

print('unt\'s 的中古音韵转写器')
print('unt 的中古音韵转写器')
print(out_str)
