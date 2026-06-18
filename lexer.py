from sly import Lexer

class ObsActLexer(Lexer):
    tokens = {"dispositivo", "word"}
    literals = {':', '{', '}', ','}

    ignore = ' \t'

    dispositivo = r'dispositivo'
    #namedevice = r'[a-zA-Z]+'
    #observation = r'[a-zA-Z]+'
    word = r'[a-zA-Z]+'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

    pass