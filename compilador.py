from lexer import ObsActLexer
from parser import ObsActParser

class Compiler():

    def __init__(self):
        self.lexer = ObsActLexer()
        self.parser = ObsActParser()

    def tokenize(self, data):
        tokens = self.lexer.tokenize(data)
        return tokens
    
    def parse(self, tokens):
        result = self.parser.parse(tokens)
        return result

    def compile(self, data):
        tokens = self.tokenize(data)
        return self.parse(tokens)
    
    def compile_from_file(self, filename):
        arq = open(filename, 'r')
        data = arq.read()
        arq.close()
        return self.compile(data)

if __name__ == '__main__':
    
    compiler = Compiler()
    result = compiler.compile_from_file('entrada.txt')
    print(result)
