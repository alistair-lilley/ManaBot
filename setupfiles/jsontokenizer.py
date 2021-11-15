'''                                                      me cri                                                      '''

ASCII = set(''.join(chr(x) for x in range(128) if chr(x) not in '"{}[],:\'\\\n '))

class Tokenizer:

    def __init__(self,filename,size):
        self.F = open(filename)
        self.block = ""
        self.index = 0
        self.readsize = size
        self._readBlock()

    def _peek(self):
        return self.block[self.index]

    def _readBlock(self):
        self.block = self.F.read(self.readsize)
        self.index = 0

    def _next(self):
        c = self.block[self.index]
        self.index += 1
        if self.index == len(self.block):
            print("Read full block")
            if self.index < self.readsize:
                return ''
            self._readBlock()
        return c

    def readToken(self):
        token = self._next()
        if not token:
            return End("END")
        elif token == '{':
            return BeginObject(token)
        elif token == '}':
            return EndObject(token)
        elif token == '[':
            return BeginArr(token)
        elif token == ']':
            return EndArr(token)
        elif token == '"':
            token = self._next()
            while self._peek() != '"':
                t = self._next()
                if t == '\\':
                    if self._peek() == '"':
                        token += self._next()
                    else:
                        self._next()
                else:
                    token += t
            return Literal(token)
        elif token in ASCII:
            while self._peek() in ASCII:
                token += self._next()
            return Literal(token)
        else:
            return Null(token)


class Token:
    def __init__(self, val):
        self.val = val

class BeginObject(Token):
    pass

class EndObject(Token):
    pass

class BeginArr(Token):
    pass

class EndArr(Token):
    pass

class Literal(Token):
    pass

class Null(Token):
    pass

class End(Token):
    pass