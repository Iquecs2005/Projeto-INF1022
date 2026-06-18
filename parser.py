from sly import Parser
from lexer import ObsActLexer

class ObsActParser(Parser):
    tokens = ObsActLexer.tokens

    @_('DEVICES')
    def PROGRAM(self, p):
        return p.DEVICES

    @_('DEVICE DEVICES')
    def DEVICES(self, p):
        return p.DEVICE + " " + p.DEVICES
    
    @_('DEVICE')
    def DEVICES(self, p):
        return p.DEVICE

    @_('dispositivo ":" "{" word "}"')
    def DEVICE(self, p):
        return p.word
    
    @_('dispositivo ":" "{" word "," word "}"')
    def DEVICE(self, p):
        return p.word0 + " " + p.word1

    pass