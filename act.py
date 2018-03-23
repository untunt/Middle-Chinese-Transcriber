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
    if s not in consonant[trans_from] and trans_from == 'zimu':
        consonant_no = consonant['vari'].index(s)
    else:
        consonant_no = consonant[trans_from].index(s)
    word[i] = consonant[trans_to][consonant_no]

output_str = ' '.join(word)

print(output_str)
