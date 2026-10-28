import enum


class TokType(enum.Enum):
    ident = 0
    number = 1
    equal = 2
    lparanthesis = 3  # (
    rparanthesis = 4  # )
    lcurly_brace = 5  # {
    rcurly_brace = 6  # }
    lsquare_brace = 7  # [
    rsquare_brace = 8  # ]
    rangle_brace = 9  # >
    star = 10
    plus = 11
    minus = 12
    slash = 13
    semicolon = 14
    unknown = 15


class Token:
    def __init__(self, kind: TokType, start: int, end: int):
        self.type: TokType = kind
        self.start: int = start
        self.end: int = end

    def __str__(self):
        return f"Token(type={self.type}, start={self.start}, end={self.end})"
