# unt's Middle Chinese Phonology Transcriber
# unt 的中古音韵转写器

import sys
from act_functions import act, print_logo

DEFAULT_IN_TYPE = 'zimu'
DEFAULT_OUT_TYPE = 'unt'
OUTPUT_FILE_NAME = 'output.txt'

print_logo()

argc = len(sys.argv)

if argc <= 1:
    in_type = input('Input type (default: ' + DEFAULT_IN_TYPE + ', press enter to use):\n>> ')
    if in_type == '':
        print('>> ' + DEFAULT_IN_TYPE)
        in_type = DEFAULT_IN_TYPE
    out_type = input('Output type (default: ' + DEFAULT_OUT_TYPE + ', press enter to use):\n>> ')
    if out_type == '':
        print('>> ' + DEFAULT_OUT_TYPE)
        out_type = DEFAULT_OUT_TYPE
    file_name = input('Read input from keyboard (press enter) or from file (input file name)?:\n>> ')
    if file_name == '':
        while True:
            in_str = input('Input (press enter to exit):\n>> ')
            if in_str == '':
                break
            print('Output:')
            print('>> ' + act(in_str, in_type, out_type))
    else:
        with open(file_name, 'r') as f1:
            with open(OUTPUT_FILE_NAME, 'w', encoding='utf_16') as f2:
                for line in f1.readlines():
                    output = act(line, in_type, out_type)
                    print(line + output)
                    f2.write(output + '\n')
        print('\nSaved as ' + OUTPUT_FILE_NAME)

else:
    in_type = DEFAULT_IN_TYPE
    out_type = DEFAULT_OUT_TYPE
    if argc > 3:
        in_type = sys.argv[3]
    if argc > 2:
        out_type = sys.argv[2]
    in_str = sys.argv[1]
