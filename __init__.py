ENCLOSED_MAP = {}#{'**': 'b', '[': 'a'}
VOID_MAP = {}#{'#': 'h', '-': 'ul'}
PAIRS = {} #{'**' : '**', '[' : ']', '(':')'}
INFO = {}#{'[' : ('(', 'href')}

# Line Tags
LINEAR_HEADERS = []#['h']
# Parent tags 
EXTENDED_HEADERS = {}#{'ul' : 'li'}

# static tags
PRAGRAPH_TAG = 'p'
BREAK_TAG = 'br'


with open('settings') as f:
    settings = f.read().splitlines()

for args in settings:
    args = args.split()
    m1 = args[0]
    tag = args[1]

    if args[-1].startswith('c='):
        EXTENDED_HEADERS[tag] = args.pop().strip('c=')
    elif len(args) == 2:
        LINEAR_HEADERS.append(tag)

    if len(args) > 2:
        ENCLOSED_MAP[m1] = tag
        PAIRS[m1] = args[2]
        if len(args) > 3:
            m3 = args[3]
            PAIRS[m3] = args[4]
            INFO[m1] = (m3, args[5])
    else:
        VOID_MAP[m1] = tag

# all marks
ENCLOSED_MARKS = list(ENCLOSED_MAP.keys())
VOID_MARKS = list(VOID_MAP.keys())