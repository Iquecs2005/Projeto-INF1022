import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lexer import ObsActLexer
from parser import ObsActParser

lexer = ObsActLexer()
parser = ObsActParser(False)

def parse(data):
    return parser.parse(lexer.tokenize(data))

def testCriaMain():
    result = parse("dispositivo : { ventilador }\nligar ventilador.")
    assert "int main()" in result
    assert "{" in result
    assert "}" in result

def testNamedevice():
    result = parse("dispositivo : { ventilador }\nligar ventilador.")
    assert 'Device ventilador = Device("ventilador")' in result

def testObservation():
    result = parse("dispositivo : { ventilador , potencia }\nligar ventilador.")
    assert 'Device ventilador = Device("ventilador", "potencia")' in result

def testDevices():
    result = parse('''dispositivo : { ventilador }
                   dispositivo : { microondas }
                   ligar ventilador.''')
    assert 'Device ventilador = Device("ventilador")' in result
    assert 'Device microondas = Device("microondas")' in result

def testCmd():
    result = parse("dispositivo : { ventilador }\nligar ventilador.")
    assert "ventilador.Ligar();" in result

def testCmds():
    result = parse('''dispositivo : { ventilador, potencia }
        set potencia = 1.
        ligar ventilador.'''
    )
    assert 'Device::GlobalSet("potencia", 1);' in result
    assert "ventilador.Ligar();" in result

def testAttribNum():
    result = parse("dispositivo : { ventilador, potencia }\nset potencia = 5.")
    assert 'Device::GlobalSet("potencia", 5);' in result

def testAttribBool():
    booleans = ["true", "True", "false", "False"]
    expected = ["true", "false"]
    for i, boolean in enumerate(booleans):
        result = parse(f"dispositivo : {{ ventilador }}\nset flag = {boolean}.")
        assert f'Device::GlobalSet("flag", {expected[i // 2]});' in result

def testAttribActexecute():
    result = parse("dispositivo : { ventilador }\nset estado = ligar ventilador.")
    assert 'Device::GlobalSet("estado", ventilador.Ligar());' in result

def testActexecuteParenteses():
    result = parse("dispositivo : { ventilador }\nligar ( ventilador ).")
    assert "ventilador.Ligar();" in result

def testActexecuteActions():
    actions = ["ligar", "desligar", "verificar"]
    expected = ["Ligar", "Desligar", "Verificar"]
    for i in range(len(actions)):
        result = parse(f"dispositivo : {{ dev }}\n{actions[i]} dev.")
        assert f"dev.{expected[i]}();" in result

def testEval():
    result = parse('''
        dispositivo : { ventilador, temperatura }
        se temperatura > 10 entao
        set x = 1.
        .'''
    )
    assert 'if (Device::GlobalGet("temperatura") > 10)' in result

def testEvalActexecute():
    result = parse('''
        dispositivo : { ventilador }
        se ligar ventilador == true entao
        set x = 1.
        .'''
    )
    assert "if (ventilador.Ligar() == true)" in result

def testConjuncao():
    result = parse('''
        dispositivo : { ventilador }
        se x >= 1 && y < 5 entao
        set z = 10.
        .'''
    )
    assert 'Device::GlobalGet("x") >= 1 && Device::GlobalGet("y") < 5' in result

def testObsact():
    result = parse('''
        dispositivo : { ventilador }
        se x == 1 entao
        set y = 2.
        .'''
    )
    assert "if (Device::GlobalGet(\"x\") == 1)" in result
    assert 'Device::GlobalSet("y", 2);' in result

def testObsactSenao():
    result = parse('''
        dispositivo : { d }
        se x == 1 entao
        set y = 2.
        senao
        set y = 0.
        .'''
    )
    assert "if (Device::GlobalGet(\"x\") == 1)" in result
    assert "else" in result
    assert 'Device::GlobalSet("y", 2);' in result
    assert 'Device::GlobalSet("y", 0);' in result

def testActalertMsg():
    result = parse('dispositivo : { ventilador }\nenviar alerta ( "aviso" ) ventilador.')
    assert 'ventilador.Alert("aviso");' in result

def testActalertMsgObservation():
    result = parse('dispositivo : { sensor, temperatura }\nenviar alerta ( "esta" , temperatura ) sensor.')
    assert 'sensor.Alert("esta", "temperatura");' in result

def testActalertTodos():
    result = parse('dispositivo : { ventilador }\nenviar alerta ( "aviso" ) para todos : a, b, c.')
    assert 'Device::AlertAll({a, b, c}, "aviso");' in result

def testActalertObservation():
    result = parse('dispositivo : { ventilador, potencia }\nenviar alerta ( "aviso" , potencia ) para todos : a, b.')
    assert 'Device::AlertAll({a, b}, "aviso", "potencia");' in result

def testVazio():
    result = parse("")
    assert result is None

def testSemDevices():
    result = parse("set x = 1.")
    assert result is None
