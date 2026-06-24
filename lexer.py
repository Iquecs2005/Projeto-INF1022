from sly import Lexer

class ObsActLexer(Lexer):
    tokens = {"dispositivo", "name", "set", "num", "bool", "action", "se", "entao", "senao", "oplogic", "conjunction"}
    literals = {':', '{', '}', ',', '.', '='}

    ignore = ' \t'

    dispositivo = r'dispositivo'
    set = r'set'

    entao = r'entao'
    senao = r'senao'
    se = r'se'

    oplogic = r'>|<|>=|<=|==|!='
    conjunction = r'&&'
    action = r'ligar|desligar|verificar'
    num = r'\d+'
    bool = r'(true|false|True|False)'
    #namedevice = r'[a-zA-Z]+'
    #observation = r'[a-zA-Z]+'
    name = r'[a-zA-Z]+'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

    pass