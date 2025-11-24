from __init__ import *

vcount = lambda line : len(line.lstrip()) - len(line.lstrip(line[0]))
icount = lambda line : (len(line) - len(line.lstrip())) // 4

class HTMLElement():
    def __init__(self, tag, token= ''):
        self.tag = tag
        self.token = token
        self.parent = None
        self.data = {}
        self.children = []

    def add_data(self, arg, value):
        self.data[arg] = value

    def add_child(self, new_child):
        if new_child not in self.children:
            if new_child: new_child.parent = self
            self.children.append(new_child)

    def add_children(self, new_children):
        if all([child not in self.children for child in new_children]):
            for child in new_children: 
                if child: child.parent = self
            self.children += new_children
        else:
            print(f"(!) Some or all of the given children are already children of ({self}).")

    def render(self):
        data = ' '.join([f"{k}=\'{v}\'" for k, v in self.data.items()])
        children = '\n'.join([child.render() for child in self.children]) if self.children else ''
        return f'<{self.tag} {data}>{self.token}{children}</{self.tag}>'

class HTMLExtended(HTMLElement):
    def __init__(self, tag, sub_tag=None, line_end=''):
        super().__init__(tag=tag, token='')
        self.lines = []
        self.sub_tag = sub_tag
        self.line_end = line_end

    def add_line(self, i):
        self.lines.append(i)
    
    def apply(self, inline_html):
        for i in self.lines:
            if type(i) == int:
                row = ''.join([part.render() for part in inline_html[i]])
                if len(self.lines) > 1 and row[-BREAK_AFTER:] == BREAK_WHITESPACE * BREAK_AFTER: 
                    row = row.rstrip(BREAK_WHITESPACE * BREAK_AFTER)
                    row += self.line_end
                
                if self.sub_tag != None:
                    element = HTMLElement(self.sub_tag, row)
                else:
                    element = EmptyElement(row)
                self.add_child(element)
            else:
                i.apply(inline_html)
                self.add_child(i)

class EmptyElement():
    def __init__(self, token= '', **info):
        self.info = info
        self.token = token
        self.children = []
    
    def add_child(self, new_child):
        if new_child not in self.children:
            if new_child: new_child.parent = self
            self.children.append(new_child)

    def add_children(self, new_children):
        if all([child not in self.children for child in new_children]):
            for child in new_children: 
                if child: child.parent = self
            self.children += new_children
        else:
            print(f"(!) Some or all of the given children are already children of ({self}).")

    def render(self):
        children = ''.join([child.render() for child in self.children])
        return f'{self.token}{children}'

class Render():
    def __init__(self, path : str):
        if not path:
            raise FileNotFoundError("(!) There no file path given.")
        try:
            with open(path, 'r') as f:
                self.txt = f.read().splitlines() 
                self.html = ''
                self.html_blocks = []
        except:
            raise FileExistsError(f"(!) the give path ({path}) doesn't not exist or may contain typo(s)")
        
    def has_enclosed_mark(self, line):
        for m in ENCLOSED_MARKS:
            if m in line:
                return True
        return False
    
    def has_void_mark(self, line):
        for m in VOID_MARKS:
            if m in line:
                return True
        return False
    
    def split_block(self):
        blocks = []
        hierarchy = {}
        last_indent = 0
        last_header = ''
        
        for i, line in enumerate(self.txt):
            if line:
                indent = icount(line)
                ls = line.lstrip() if indent else line
                repeat = vcount(ls)
                m = ls[0]

                header = VOID_MAP.get(m)
                if not AUTO_WHITESPACE_PROCESS and header != None:
                    if ls.lstrip(m)[0] != SPACE:
                        header = 'misformat'
                        print(f'(!) line-{i}:\n{self.txt[i]}\n got a misformated mark ({m}).') 
                # test if there is any single-line header
                if header in LINEAR_HEADERS:
                    block = HTMLExtended(tag=f'{header}{repeat}' if repeat else header)        
                    block.add_line(i)
                    blocks.append(block)
                    hierarchy[indent] = None
                # if not, look for any extended header
                else:
                    if indent > last_indent or header != last_header:
                        if header in EXTENDED_HEADERS:
                            sub_tag = EXTENDED_HEADERS[header]
                            block = HTMLExtended(tag=header, sub_tag=sub_tag)
                        else:
                            block = HTMLExtended(tag=PRAGRAPH_TAG, line_end=f'<{BREAK_TAG}>')
                        hierarchy[indent] = block
                        block.add_line(i)

                        if indent > 0 and hierarchy[indent - 1] != None:
                            try:
                                hierarchy[indent - 1].add_line(block)
                            except:
                                raise IndentationError(f"line-{i} is not aligned correctly.\n(!){line}")
                        else:
                            blocks.append(block)
                    elif hierarchy[indent] != None:
                        try:
                            hierarchy[indent].add_line(i)
                        except:
                            raise IndentationError(f"line-{i} is not aligned correctly.\n(!){line}")
           
                last_indent = indent
                last_header = header
            else:
                last_indent = 0
                last_header = ''

        return blocks

    def split_line(self, line : str):
        pattren = [(line.find(m), len(m)) for m in ENCLOSED_MARKS if m in line]
        if pattren:
            minimum = min(pattren, key= lambda x:x[0])
            m = line[minimum[0]:sum(minimum)]
            em = PAIRS[m]

            parts = line.split(m, 1)
            parts[1:] = parts[1].split(em, 1)
 
            tag = ENCLOSED_MAP[m]
            p1 = HTMLElement(tag, parts[1])
            
            if self.has_enclosed_mark(parts[1]):
                p1.add_children(self.split_line(parts[1]))
                p1.token = ''

            if INFO.get(m):
                m1, arg = INFO[m]
                em1 = PAIRS[m1]
                info = parts[2].split(m1, 1)[1].split(em1, 1)[0]
                parts[2] = parts[2].split(em1, 1)[1]
                p1.add_data(arg, info)

            if parts[0]:
                return [EmptyElement(parts[0]), p1] + self.split_line(parts[2])
            return [p1] + self.split_line(parts[2])
        
        elif self.has_void_mark(line):
            ls = line.lstrip()
            return [EmptyElement(ls[vcount(ls):])]
        
        return [EmptyElement(line)]

    def render_veiw(self):
        inline_html = []
        is_false = False
        
        for line in self.txt:
            # striping out void marks from the line
            if line:
                m = line.lstrip()[0]
                if m in VOID_MARKS:
                    if not AUTO_WHITESPACE_PROCESS:
                        if line.lstrip().lstrip(m)[0] == SPACE:
                            line = line.lstrip(m)
                        else:
                            is_false = True
                else:
                    is_false = False
                row_html = self.split_line(line)
                if is_false:            
                    row_html[0].token = m + row_html[0].token 
                inline_html.append(row_html)
            else:
                inline_html.append([EmptyElement('\n')])

        self.html_blocks = self.split_block()
        [block.apply(inline_html) for block in self.html_blocks] 
        
        # render
        self.html += '\n'.join([block.render() for block in self.html_blocks])
        print(f'(*) The file is successfully rendered into html.')

    def write(self, path):
        if not self.html:
            print("(!!) There no html stored.\ntry:\nrender_view()")
        try:
            with open(path, 'w') as f:
                f.write(self.html)
        except:
            with open(path, 'x') as f:
                f.write(self.html)
        print(f"(*) The html is written at [{path}].")