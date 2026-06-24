from lexer import ObsActLexer
from parser import ObsActParser

class Compiler():

    def __init__(self):
        self.lexer = ObsActLexer()
        self.parser = ObsActParser(False)

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
    
    def compile_to_file(self, input_filename, output_filename):
        result = self.compile_from_file(input_filename)

        base = open("compiler/base.cpp", 'r')
        baseContent = base.read()
        base.close()

        with open(output_filename + '.cpp', 'w') as f:
            f.write(baseContent + "\n")
            f.write(result)

if __name__ == '__main__':
    
    compiler = Compiler()
    result = compiler.compile_to_file('entrada.txt', 'saida')
    print(result)
