# unt's Ancient (Middle) Chinese Phonology Transcriber
# unt 的中古音韵转写器

import sys
from act_functions import act

DEFAULT_IN_TYPE = 'zimu'
DEFAULT_OUT_TYPE = 'unt'

print("""
====================================
   unt's Ancient (Middle) Chinese
        Phonology Transcriber

         unt 的中古音韵转写器
====================================
""")

argc = len(sys.argv)

while True:
    if argc <= 1:
        in_str = input("Input (press enter to exit):\n>> ")
        if in_str == "":
            break
        in_type = input("Input type (default: " + DEFAULT_IN_TYPE + ", press enter to use):\n>> ")
        if in_type == "":
            print(">> " + DEFAULT_IN_TYPE)
            in_type = DEFAULT_IN_TYPE
        out_type = input("Output type (default: " + DEFAULT_OUT_TYPE + ", press enter to use):\n>> ")
        if out_type == "":
            print(">> " + DEFAULT_OUT_TYPE)
            out_type = DEFAULT_OUT_TYPE
    else:
        in_type = DEFAULT_IN_TYPE
        out_type = DEFAULT_OUT_TYPE
        if argc > 3:
            in_type = sys.argv[3]
        if argc > 2:
            out_type = sys.argv[2]
        in_str = sys.argv[1]

    print("Output:")
    print(">> " + act(in_str, in_type, out_type))

    if argc > 1:
        break
