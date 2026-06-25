import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lexer import ObsActLexer

lexer = ObsActLexer()

def tokenize(data):
    tokens = lexer.tokenize(data)
    return [(tok.type, tok.value) for tok in tokens]

def testID():
    tokens = tokenize("temperatura")
    assert tokens == [("ID", "temperatura")]

def testNumPositivo():
    tokens = tokenize("42")
    assert tokens == [("NUM", "42")]

def testZero():
    tokens = tokenize("0")
    assert tokens == [("NUM", "0")]

# nesse teste o sinal de negativo e um caracter ignorado entao o que tem que ser lido e o numero 1
def testNumNegativo():
    tokens = tokenize("-1")
    assert tokens == [("NUM", "1")]

def testTrueMinusculo():
    tokens = tokenize("true")
    assert tokens == [("BOOL", "true")]

def testFalseMinusculo():
    tokens = tokenize("false")
    assert tokens == [("BOOL", "false")]

def testTrueMaiusculo():
    tokens = tokenize("True")
    assert tokens == [("BOOL", "True")]

def testFalseMaiusculo():
    tokens = tokenize("False")
    assert tokens == [("BOOL", "False")]

def testActionLigar():
    tokens = tokenize("ligar")
    assert tokens == [("ACTION", "ligar")]

def testActionDesligar():
    tokens = tokenize("desligar")
    assert tokens == [("ACTION", "desligar")]

def testActionVerificar():
    tokens = tokenize("verificar")
    assert tokens == [("ACTION", "verificar")]

def test_palavras_reservadas():
    words = ["dispositivo", "set", "se", "entao", "senao", "enviar", "alerta"]
    for word in words:
        tokens = tokenize(word)
        assert tokens == [(word, word)]

def testOplogic():
    operaddores = [">", "<", ">=", "<=", "==", "!="]
    for op in operaddores:
        tokens = tokenize(op)
        assert tokens == [(op, op)]

def testConjunction():
    tokens = tokenize("&&")
    assert tokens == [("CONJUNCTION", "&&")]

# teste da mensagem

def testLiterais():
    literais = [":", "{", "}", ",", ".", "=", "(", ")"]
    for literal in literais:
        tokens = tokenize(literal)
        assert tokens == [(literal, literal)]

def testEspacos():
    tokens = tokenize("set   nome")
    assert tokens == [("set", "set"), ("ID", "nome")]

def testTab():
    tokens = tokenize("set\tnome")
    assert tokens == [("set", "set"), ("ID", "nome")]

# linha nova
# caracter errado