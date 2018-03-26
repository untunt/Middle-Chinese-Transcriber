import sys
from list import *

argc = len(sys.argv)
if argc > 3:
    trans_to = sys.argv[3]
else:
    trans_to = 'poly' # 'ipa_u'
if argc > 2:
    trans_from = sys.argv[2]
else:
    trans_from = 'zimu'
input_str = sys.argv[1]

word = input_str.split()
for i, s in enumerate(word):
    c = s[0]
    v = s[-1]
    if c not in consonant[trans_from] and trans_from == 'zimu':
        c_index = consonant['vari'].index(c)
    else:
        c_index = consonant[trans_from].index(c)
    if v not in vowel[trans_from] and trans_from == 'zimu':
        v_index = consonant['vari'].index(v)
    else:
        v_index = consonant[trans_from].index(v)
    word[i] = consonant[trans_to][c_index] + vowel[trans_to][v_index]

output_str = ' '.join(word)

print(output_str)
