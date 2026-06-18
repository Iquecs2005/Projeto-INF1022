from lexer import ObsActLexer
#from parser import ObsActParser

lexer = ObsActLexer()
#parser = ObsActParser()

arq = open('entrada.txt', 'r')

data = arq.read()
for tok in lexer.tokenize(data):
    print(tok)

arq.close()