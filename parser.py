from sly import Parser
from lexer import ObsActLexer

class ObsActParser(Parser):
    tokens = ObsActLexer.tokens

    @_('DEVICES CMDS')
    def PROGRAM(self, p):
        return p.DEVICES + "\n" + p.CMDS

    @_('DEVICE DEVICES')
    def DEVICES(self, p):
        return p.DEVICE + "\n" + p.DEVICES
    
    @_('DEVICE')
    def DEVICES(self, p):
        return p.DEVICE

    @_('dispositivo ":" "{" name "}"')
    def DEVICE(self, p):
        return p.name
    
    @_('dispositivo ":" "{" name "," name "}"')
    def DEVICE(self, p):
        return p.name0 + " " + p.name1

    @_('CMD "." CMDS')
    def CMDS(self, p):
        return p.CMD + ".\n" + p.CMDS

    @_('CMD "."')
    def CMDS(self, p):
        return p.CMD + "."

    @_('ATTRIB')
    def CMD(self, p):
        return p.ATTRIB
    
    @_('OBSACT')
    def CMD(self, p):
        return p.OBSACT
    
    # @_('ACT')
    # def CMD(self, p):
    #     return p.ACT

    @_('set name "=" VAR')
    def ATTRIB(self, p):
        return p.set + " " + p.name + " = " + p.VAR
    
    @_('set name "=" ACTEXECUTE')
    def ATTRIB(self, p):
        return p.set + " " + p.name + " = " + p.ACTEXECUTE
    
    @_('se OBS entao CMDS')
    def OBSACT(self, p):
        return p.se + " " + p.OBS + " " + p.entao + " " + p.CMDS + "fimse"
    
    @_('se OBS entao CMDS senao CMDS')
    def OBSACT(self, p):
        return f"{p.se} {p.OBS} {p.entao} {p.CMDS0} {p.senao} {p.CMDS1} fimse"

    @_('name oplogic VAR')
    def OBS(self, p):
        return p.name + " " + p.oplogic + " " + p.VAR

    @_('num')
    def VAR(self, p):
        return p.num

    @_('bool')
    def VAR(self, p):
        return p.bool
    
    @_('ACTION name')
    def ACTEXECUTE(self, p):
        return p.ACTION + " " + p.name

    @_('action')
    def ACTION(self, p):
        return p.action

    pass