from sly import Parser
from lexer import ObsActLexer

class ObsActParser(Parser):
    debugfile = "parser.out"

    tokens = ObsActLexer.tokens

    @_('DEVICES CMDS')
    def PROGRAM(self, p):
        code = f'''
int main()
{{
    {p.DEVICES}
    {p.CMDS}
}}'''

        return code

    @_('DEVICE DEVICES')
    def DEVICES(self, p):
        return p.DEVICE + ";\n\t" + p.DEVICES
    
    @_('DEVICE')
    def DEVICES(self, p):
        return p.DEVICE + ";"

    @_('dispositivo ":" "{" ID "}"')
    def DEVICE(self, p):
        return f"Device {p.ID} = Device(\"{p.ID}\")"
    
    @_('dispositivo ":" "{" ID "," ID "}"')
    def DEVICE(self, p):
        return f"Device {p.ID0} = Device(\"{p.ID0}\", \"{p.ID1}\")"

    @_('CMD "." CMDS')
    def CMDS(self, p):
        return p.CMD + ";\n\t" + p.CMDS

    @_('CMD "."')
    def CMDS(self, p):
        return p.CMD + ";"

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
        return f"Device::GlobalSet(\"{p.ID}\", {p.VAR})"
    
    @_('set ID "=" ACTEXECUTE')
    def ATTRIB(self, p):
        return f"Device::GlobalSet(\"{p.ID}\", {p.ACTEXECUTE})"
    
    @_('se OBS entao CMDS')
    def OBSACT(self, p):
        code = f'''
if ({p.OBS}) 
{{
    {p.CMDS}
}}       
'''
        return code
    
    @_('se OBS entao CMDS senao CMDS')
    def OBSACT(self, p):
        code = f'''
if ({p.OBS}) 
{{
    {p.CMDS0}
}}
else
{{
    {p.CMDS1}
}}       
'''
        return code

    @_('EVAL OPLOGIC VAR')
    def OBS(self, p):
        code = f'''{p.EVAL} {p.OPLOGIC} {p.VAR}'''
        return code
    
    @_('EVAL OPLOGIC VAR CONJUNCTION OBS')
    def OBS(self, p):
        code = f'''{p.EVAL} {p.OPLOGIC} {p.VAR} && {p.OBS}'''
        return code
    
    @_('ID')
    def EVAL(self, p):
        return f'''Device::GlobalGet(\"{p.ID}\")'''

    @_('ACTEXECUTE')
    def EVAL(self, p):
        return p.ACTEXECUTE

    @_('NUM')
    def VAR(self, p):
        return p.NUM

    @_('BOOL')
    def VAR(self, p):
        return p.BOOL.lower()
    
    @_('ACTEXECUTE')
    def ACT(self, p):
        return f"{p.ACTEXECUTE}"
    
    @_('ACTALERT')
    def ACT(self, p):
        return f"{p.ACTALERT}"

    @_('ACTION ID')
    def ACTEXECUTE(self, p):
        return f"{p.ID}.{p.ACTION.capitalize()}()"
    
    @_('ACTION "(" ID ")"')
    def ACTEXECUTE(self, p):
        return f"{p.ID}.{p.ACTION.capitalize()}()"
    
    @_('enviar alerta "(" MSG ")" ID')
    def ACTALERT(self, p):
        return f"{p.ID}.Alert({p.MSG})"
    
    @_('enviar alerta "(" MSG "," ID ")" ID')
    def ACTALERT(self, p):
        return f"{p.ID1}.Alert({p.MSG}, \"{p.ID0}\")"
    
    @_('enviar alerta "(" MSG ")" para todos : TARGET')
    def ACTALERT(self, p):
        return f"Device::AlertAll({{{p.TARGET}}}, {p.MSG})"
    
    @_('enviar alerta "(" MSG "," ID ")" para todos : TARGET')
    def ACTALERT(self, p):
        return f"Device::AlertAll({{{p.TARGET}}}, {p.MSG}, \"{p.ID}\")"
    
    @_('ID "," TARGET')
    def TARGET(self, p):
        return f"{p.ID}, {p.TARGET}"
    
    @_('ID')
    def TARGET(self, p):
        return f"{p.ID}"

    pass