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

    @_('dispositivo ":" "{" ID "}"')
    def DEVICE(self, p):
        return p.ID
    
    @_('dispositivo ":" "{" ID "," ID "}"')
    def DEVICE(self, p):
        return p.ID0 + " " + p.ID1

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

    @_('set ID "=" VAR')
    def ATTRIB(self, p):
        return p.set + " " + p.ID + " = " + p.VAR
    
    @_('set ID "=" ACTEXECUTE')
    def ATTRIB(self, p):
        return p.set + " " + p.ID + " = " + p.ACTEXECUTE
    
    @_('se OBS entao CMDS')
    def OBSACT(self, p):
        return p.se + " " + p.OBS + " " + p.entao + " " + p.CMDS + "fimse"
    
    @_('se OBS entao CMDS senao CMDS')
    def OBSACT(self, p):
        return f"{p.se} {p.OBS} {p.entao} {p.CMDS0} {p.senao} {p.CMDS1} fimse"

    @_('ID OPLOGIC VAR')
    def OBS(self, p):
        return p.ID + " " + p.OPLOGIC + " " + p.VAR
    
    @_('ID OPLOGIC VAR CONJUNCTION OBS')
    def OBS(self, p):
        return f"{p.ID} {p.OPLOGIC} {p.VAR} {p.CONJUNCTION} {p.OBS}"

    @_('NUM')
    def VAR(self, p):
        return p.NUM

    @_('BOOL')
    def VAR(self, p):
        return p.BOOL
    
    @_('ACTEXECUTE')
    def ACT(self, p):
        return f"{p.ACTEXECUTE}"
    
    @_('ACTALERT')
    def ACT(self, p):
        return f"{p.ACTALERT}"

    @_('ACTION ID')
    def ACTEXECUTE(self, p):
        return p.ACTION + " " + p.ID
    
    @_('enviar alerta "(" ID ")" ID')
    def ACTALERT(self, p):
        return f"{p.enviar} {p.alerta} ({p.ID0}) {p.ID1}"
    
    @_('enviar alerta "(" ID "," ID ")" ID')
    def ACTALERT(self, p):
        return f"{p.enviar} {p.alerta} ({p.ID0}, {p.ID1}) {p.ID2}"

    pass