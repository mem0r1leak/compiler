from token import TokType, Token

alphabet_lowercase = 'qwertyuiopasdfghjklzxcvbnm'
alphabet_uppercase = alphabet_lowercase.upper()
alphabet = alphabet_lowercase + alphabet_uppercase
numbers = '0123456789'

def state_from_char(char: str):
    return {
        '(': TokType.lparanthesis,
        ')': TokType.rparanthesis,
        '[': TokType.lsquare_brace,
        ']': TokType.rsquare_brace,
        '{': TokType.lcurly_brace,
        '}': TokType.rcurly_brace,
        '>': TokType.rangle_brace,
        '=': TokType.equal,
        ';': TokType.semicolon,
        '*': TokType.star,
        '/': TokType.slash,
        '-': TokType.minus,
        '+': TokType.plus,
    }.get(char)


class Tokenizer:
    def __init__(self):
        self.tokens: list[Token] = []
        self.pos: int = 0
        self.base: int = 0
        self.state = TokType.unknown

    def emit(self):
        self.tokens.append(Token(self.state, self.base, self.pos))
        self.base = self.pos

    def tokenize(self, source: str) -> list[Token]:
        while self.pos < len(source):
            if source[self.pos] in numbers + '.':
                while source[self.pos] in numbers + '.':
                    self.pos += 1
                self.state = TokType.number
                self.emit()
            elif source[self.pos] in alphabet + numbers + '.':
                while source[self.pos] in alphabet + numbers + '.':
                    self.pos += 1
                self.state = TokType.ident
                self.emit()
            elif source[self.pos] in ';=[]{}()>*/+-':
                self.state = state_from_char(source[self.pos])
                self.pos += 1
                self.emit()
            elif source[self.pos] in ' \r\n':
                self.base += 1
                self.pos += 1
            else:
                self.state = TokType.unknown
                self.pos += 1
        return self.tokens
