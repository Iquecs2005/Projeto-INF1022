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
    
    @_('ACT')
    def CMD(self, p):
        return p.ACT

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
    
    @_('name oplogic VAR conjunction OBS')
    def OBS(self, p):
        return f"{p.name} {p.oplogic} {p.VAR} {p.conjunction} {p.OBS}"

    @_('num')
    def VAR(self, p):
        return p.num

    @_('bool')
    def VAR(self, p):
        return p.bool
    
    @_('ACTEXECUTE')
    def ACT(self, p):
        return f"{p.ACTEXECUTE}"
    
    @_('ACTALERT')
    def ACT(self, p):
        return f"{p.ACTALERT}"

    @_('ACTION name')
    def ACTEXECUTE(self, p):
        return p.ACTION + " " + p.name
    
    @_('enviar alerta "(" name ")" name')
    def ACTALERT(self, p):
        return f"{p.enviar} {p.alerta} ({p.name0}) {p.name1}"
    
    @_('enviar alerta "(" name "," name ")" name')
    def ACTALERT(self, p):
        return f"{p.enviar} {p.alerta} ({p.name0}, {p.name1}) {p.name2}"

    @_('action')
    def ACTION(self, p):
        return p.action

    pass