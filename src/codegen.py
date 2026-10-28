from token import Token, TokType

class Codegen:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def get_tok(self, offset = 0):
        return self.tokens[self.pos+offset]

    def expect(self, tok_type):
        if self.get_tok().type != tok_type:
            raise Exception(f'Expected {tok_type}, got {self.get_tok().type}')

    def evaluate_expr(self):
        while self.get_tok(0).type in [TokType.minus, TokType.plus,
                                  TokType.star, TokType.slash, TokType.number,
                                  TokType.ident, TokType.rparanthesis, TokType.lparanthesis]:
            pass

    def get_precedence(self, tok: Token):
        match tok.type:
            case TokType.minus, TokType.plus:
                return 1
            case TokType.star, TokType.slash:
                return 2
            case TokType.lparanthesis, TokType.rparanthesis:
                return 0
        return None

    def eval(self):
        operators = []
        operations = []

        while self.get_precedence(operations[-1]) < self.get_tok(0):
            pass

    def translate(self):
        pass

    def translate_expression(self):
        pass
