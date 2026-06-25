import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lexer import ObsActLexer
from parser import ObsActParser
from compilador import Compiler, CompilerError

lexer = ObsActLexer()
parser = ObsActParser()
compiler = Compiler()

def fuzzy_str_compare(str1, str2):
    cleanStr1 = str1.replace("\n", "").replace("\t", "").replace(" ", "")
    cleanStr2 = str2.replace("\n", "").replace("\t", "").replace(" ", "")
    return cleanStr1 == cleanStr2

def test_tokenize():
    code = '''
        dispositivo : { Termometro , temperatura }
        dispositivo : { ventilador , potencia }
        set temperatura = 40.
        set potencia = 90.
        se temperatura > 30 entao 
            ligar ventilador .
        .
    '''
    compilerTokens = list(compiler.tokenize(code))
    lexerTokens = list(lexer.tokenize(code))

    for i in range(len(compilerTokens)):
        assert compilerTokens[i].type == lexerTokens[i].type
        assert compilerTokens[i].value == lexerTokens[i].value

def test_parse():
    code = '''
        dispositivo : { Termometro , temperatura }
        dispositivo : { ventilador , potencia }
        set temperatura = 40.
        set potencia = 90.
        se temperatura > 30 entao 
            ligar ventilador .
        .
    '''
    tokens = lexer.tokenize(code)
    compilerParse = compiler.parse(tokens)
    tokens = lexer.tokenize(code)
    parserParse = parser.parse(tokens)

    assert compilerParse == parserParse

def test_compile_example_1():
    code = '''
        dispositivo : { Termometro , temperatura }
        dispositivo : { ventilador , potencia }
        set temperatura = 40.
        set potencia = 90.
        se temperatura > 30 entao 
            ligar ventilador .
        .
    '''
    assert compiler.compile(code) is not None

def test_compile_example_2():
    code = '''
        dispositivo : { Termometro , temperatura }
        dispositivo : { ventilador , potencia }
        set temperatura = 40.

        se temperatura > 30 entao
            set estado_ventilador = verificar ( ventilador ) .
            se estado_ventilador == 0 entao 
                ligar ventilador.
                set potencia = 90.
            .
        .
    '''
    assert compiler.compile(code) is not None

def test_compile_example_3():
    code = '''
        dispositivo : { monitor }
        dispositivo : { celular }
        dispositivo : { Termometro , temperatura }

        se temperatura > 30 entao
            enviar alerta (" Temperatura em " , temperatura ) para todos : monitor , celular .
        .
    '''
    assert compiler.compile(code) is not None

def test_compile_example_4():
    code = '''
        dispositivo : { celular , movimento }
        dispositivo : { higrometro , umidade }
        dispositivo : { lampada , potencia }
        dispositivo : { Monitor }
        set potencia = 100 .
        se umidade < 40 entao
            enviar alerta ( " Ar seco detectado " ) Monitor .
        .
        se movimento == True entao
            ligar lampada .
        senao
            desligar lampada .
        .
    '''
    assert compiler.compile(code) is not None

def test_compile_example_5():
    code = '''
        dispositivo : { umidade }
        dispositivo : { Monitor }
        se umidade < 40 entao
            enviar alerta ( " Ar seco detectado " ) Monitor .
        .
    '''
    assert compiler.compile(code) is not None

def test_compile_example_6():
    code = '''
        dispositivo : { lampada , potencia }
        set potencia = 100.
        ligar lampada.
    '''
    assert compiler.compile(code) is not None

def test_compile_example_7():
    code = '''
        dispositivo : { ventilador }
        desligar ventilador.
    '''
    assert compiler.compile(code) is not None

def test_compile_example_8():
    code = '''
        dispositivo : { Celular }
        enviar alerta (" Hora de acordar !") Celular.
    '''
    assert compiler.compile(code) is not None

def test_compile_example_9():
    code = '''
        dispositivo : { Termometro , temperatura }
        enviar alerta (" Temperatura esta em " , temperatura ) Termometro.
    '''
    expected_code = ''' 
        int main()
        {
            Device Termometro = Device("Termometro", "temperatura");
            Termometro.Alert(" Temperatura esta em " , "temperatura");
        }
    '''
    compiled_code = compiler.compile(code)
    assert compiled_code is not None
    assert fuzzy_str_compare(compiled_code, expected_code)

def test_compile_unsucessfull():
    unsucessfullCode = 'isso deveria dar erro .'
    assert compiler.compile(unsucessfullCode) is None

def test_compile_from_file():
    file_path = "arquivoTeste.txt"
    if os.path.isfile(file_path):
        os.remove(file_path)

    with pytest.raises(FileNotFoundError):
        compiler.compile_from_file(file_path)
    
    unsucessfull_code = 'isso deveria dar erro .'
    with open(file_path, 'w') as f:
        f.write(unsucessfull_code)

    assert compiler.compile_from_file(file_path) is None

    sucessfull_code = '''
        dispositivo : { Termometro , temperatura }
        enviar alerta (" Temperatura esta em " , temperatura ) Termometro.
    '''
    expected_code = ''' 
        int main()
        {
            Device Termometro = Device("Termometro", "temperatura");
            Termometro.Alert(" Temperatura esta em " , "temperatura");
        }
    '''
    with open(file_path, 'w') as f:
        f.write(sucessfull_code)

    compiled_code = compiler.compile_from_file(file_path)
    assert fuzzy_str_compare(compiled_code, expected_code)

    if os.path.isfile(file_path):
        os.remove(file_path)

def test_compile_to_file():
    input_file_path = "arquivoEntradaTeste.txt"
    output_file_path = "arquivoSaidaTeste.cpp"

    if os.path.isfile(input_file_path):
        os.remove(input_file_path)

    with pytest.raises(FileNotFoundError):
        compiler.compile_to_file(input_file_path, output_file_path)
    
    unsucessfull_code = 'isso deveria dar erro .'
    with open(input_file_path, 'w') as f:
        f.write(unsucessfull_code)

    with pytest.raises(CompilerError):
        compiler.compile_to_file(input_file_path, output_file_path)

    sucessfull_code = '''
        dispositivo : { Termometro , temperatura }
        enviar alerta (" Temperatura esta em " , temperatura ) Termometro.
    '''
    
    f = open("compiler/base.cpp", 'r')
    base_code = f.read()
    f.close()

    expected_code = base_code + '''\n\n 
        int main()
        {
            Device Termometro = Device("Termometro", "temperatura");
            Termometro.Alert(" Temperatura esta em " , "temperatura");
        }
    '''
    with open(input_file_path, 'w') as f:
        f.write(sucessfull_code)

    compiler.compile_to_file(input_file_path, output_file_path)
    with open(output_file_path, 'r') as f:
        fileContents = f.read()
        assert fuzzy_str_compare(fileContents, expected_code)

    if os.path.isfile(input_file_path):
        os.remove(input_file_path)
    if os.path.isfile(output_file_path):
        os.remove(output_file_path)