import sys
from list import *

input_str = sys.argv[1]

word = input_str.split()
for i, s in enumerate(word):
    consonant_no = consonant['zimu'].index(s)
    word[i] = consonant['poly'][consonant_no]

output_str = ' '.join(word)

print(output_str)
