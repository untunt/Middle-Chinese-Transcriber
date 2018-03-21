import sys

# 声母
consonant = {
    'zimu': [
        '帮', '滂', '並', '明',
        '端', '透', '定', '泥',
        '知', '彻', '澄', '娘',
        '见', '溪', '群', '疑',
        '精', '清', '从', '心', '邪',
        '庄', '初', '崇', '生', '俟',
        '章', '昌', '常', '书', '船',
        '晓', '匣', '影', '云', '以',
        '来',
        '日',
        '非', '敷', '奉', '微',
        '照', '穿', '床', '审', '禅',
        '喻'
    ],
    'poly': [
        'p', 'ph', 'b', 'm',
        't', 'th', 'd', 'n',
        'tr', 'thr', 'dr', 'nr',
        'k', 'kh', 'g', 'ng',
        'c', 'ch', 'z', 's', 'zs',
        'cr', 'chr', 'zr', 'sr', 'zsr',
        'cj', 'chj', 'zj', 'sj', 'zsj',
        'h', 'gh', 'q', '', 'j',
        'l',
        'nj',
        '', '', '', '',
        '', '', '', '', '',
        ''
    ]
}

input_str = sys.argv[1]

word = input_str.split()
for i, s in enumerate(word):
    consonant_no = consonant['zimu'].index(s)
    word[i] = consonant['poly'][consonant_no]

output_str = ' '.join(word)

print(output_str)
