from primitives import Token, TokType


def get_precedence(tok: Token):
    match tok.type:
        case TokType.minus | TokType.plus:
            return 1
        case TokType.star | TokType.slash:
            return 2
        case TokType.lparanthesis | TokType.rparanthesis:
            return 0
        case TokType.unary_minus:
            return 3
    raise Exception(f'Unexpected token: {tok}')


def is_operator(tok: Token):
    return tok.type in {TokType.plus, TokType.minus, TokType.star, TokType.slash}


def is_value(tok: Token):
    return tok.type == TokType.number or tok.type == TokType.ident


def is_expression(tok: Token):
    return is_operator(tok) or is_value(tok) or tok.type in {
        TokType.lparanthesis,
        TokType.rparanthesis}


def translate_opcode(operator: TokType):
    return {TokType.plus: "add", TokType.minus: "sub", TokType.star: "mul", TokType.slash: "div"}[operator]


class Instruction:
    def __init__(self, opcode: str, *args):
        self.opcode = opcode
        self.args = [*args]

    def __str__(self):
        return f'{self.opcode} {' '.join(map(str, self.args))}'


class Codegen:
    def __init__(self, tokens: list[Token], code: str):
        self.tokens = tokens
        self.pos = 0
        self.code = code
        self.var_counter = 0
        self.instructions = []

    def get_tok(self, offset: int = 0) -> Token:
        return self.tokens[self.pos + offset]

    def has_tokens(self):
        return self.pos < len(self.tokens)

    def take_tok(self) -> Token:
        val = self.get_tok()
        self.pos += 1
        return val

    def tok_value(self, tok: Token) -> str:
        return self.code[tok.start:tok.end]

    def expect(self, tok_type: TokType):
        if self.get_tok().type != tok_type:
            raise Exception(f'Expected {tok_type}, got {self.get_tok().type}')

    def expect_take(self, tok_type: TokType):
        if self.get_tok().type != tok_type:
            raise Exception(f'Expected {tok_type}, got {self.get_tok().type}')
        self.take_tok()

    def get_temp_variable(self):
        var_name = f't{self.var_counter}'
        self.var_counter += 1
        return var_name

    def get_instructions(self):
        return self.instructions

    def translate_condition(self):
        self.expect(TokType.lsquare_brace)
        self.take_tok()
        self.translate_expression()
        self.expect(TokType.rsquare_brace)
        self.take_tok()

    def translate_conditional_body(self, inverse_condition):
        self.instructions.append(
            Instruction('gotoif' if inverse_condition else 'gotoifnot', f't{self.var_counter - 1}', 0))
        goto_ins = self.instructions[-1]
        self.expect_take(TokType.lcurly_brace)
        self.translate_stmt()
        self.expect_take(TokType.rcurly_brace)
        goto_ins.args[1] = len(self.instructions) + 1

    def translate_loop(self, inverse_condition: bool):
        self.translate_condition()
        loop_start = len(self.instructions) - 1
        self.translate_conditional_body(inverse_condition)
        self.instructions.append(Instruction('goto', loop_start))

    def translate_if(self, inverse_condition: bool):
        self.translate_condition()
        self.translate_conditional_body(inverse_condition)

    def translate_stmt(self):
        while self.has_tokens() and self.get_tok().type not in {TokType.rcurly_brace, TokType.semicolon}:
            self.expect(TokType.ident)
            tok = self.take_tok()
            tok_value = self.tok_value(tok)
            if tok_value in {'write', 'read'}:
                self.expect_take(TokType.rangle_brace)
                literal = self.take_tok()
                self.expect_take(TokType.semicolon)
                self.instructions.append(Instruction(tok_value, self.tok_value(literal)))
            elif tok_value == 'if':
                self.translate_if(False)
            elif tok_value == 'ifnot':
                self.translate_if(True)
            elif tok_value == 'while':
                self.translate_loop(False)
            elif tok_value == 'whilenot':
                self.translate_loop(True)
            elif self.take_tok().type == TokType.equal:
                self.translate_expression()
                self.instructions.append(Instruction('copy', f't{self.var_counter - 1}', tok_value))
                self.expect_take(TokType.semicolon)
            else:
                raise Exception("Expected keyword, got " + str(self.take_tok().type))

    def translate(self):
        while self.has_tokens():
            self.translate_stmt()

    def translate_expression(self):
        operators = []
        operands = []

        def negate(s):
            return s[1:] if s.startswith("-") else "-" + s

        def pop_operand():
            if not operands:
                raise Exception("Syntax error: missing operand")
            return operands.pop()

        def apply_operator():
            op_tok = operators.pop()

            if op_tok.type == TokType.unary_minus:
                operands.append(negate(pop_operand()))
                return

            right = pop_operand()
            left = pop_operand()
            result = self.get_temp_variable()
            self.instructions.append(
                Instruction(translate_opcode(op_tok.type), left, right, result)
            )
            operands.append(result)

        while self.has_tokens():
            tok = self.get_tok()

            if is_value(tok):
                operands.append(self.tok_value(self.take_tok()))
            elif tok.type == TokType.unary_minus:
                operators.append(self.take_tok())
            elif tok.type == TokType.lparanthesis:
                operators.append(self.take_tok())
            elif tok.type == TokType.rparanthesis:
                self.take_tok()
                while operators and operators[-1].type != TokType.lparanthesis:
                    apply_operator()
                if not operators:
                    raise Exception("Mismatched parentheses: missing '('")
                operators.pop()
            elif is_operator(tok):
                prec = get_precedence(tok)
                while (operators
                       and operators[-1].type != TokType.lparanthesis
                       and get_precedence(operators[-1]) >= prec):
                    apply_operator()
                operators.append(self.take_tok())
            else:
                break

        while operators:
            if operators[-1].type == TokType.lparanthesis:
                raise Exception("Mismatched parentheses: missing ')'")
            apply_operator()

        return pop_operand()
