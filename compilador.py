from lexer import ObsActLexer
from parser import ObsActParser

if __name__ == '__main__':
    
    lexer = ObsActLexer()
    parser = ObsActParser()

    arq = open('entrada.txt', 'r')

    data = arq.read()

    tokens = lexer.tokenize(data)
    result = parser.parse(tokens)

    print(result)

    arq.close()