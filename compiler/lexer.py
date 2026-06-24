from sly import Lexer

class ObsActLexer(Lexer):
    basicTokens = {"ID", "NUM", "BOOL", "ACTION", "OPLOGIC", "CONJUNCTION"} 
    reservedWords = {"dispositivo", "set", "se", "entao", "senao", "enviar", "alerta"}
    specialWords = {"ligar" : "ACTION",
                    "desligar" : "ACTION",
                    "verificar" : "ACTION",
                    "true" : "BOOL",
                    "false" : "BOOL",
                    "True" : "BOOL",
                    "False" : "BOOL"}
    tokens = basicTokens | reservedWords

    literals = {':', '{', '}', ',', '.', '=', '(', ')'}
    ignore = ' \t'

    OPLOGIC = r'>|<|>=|<=|==|!='
    CONJUNCTION = r'&&'
    NUM = r'\d+'
    ID = r'[a-zA-Z]+'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

    def ID(self, t):
        if t.value in self.specialWords:
            t.type = self.specialWords[t.value]
        elif t.value in self.reservedWords:
            t.type = t.value
        return t

    pass