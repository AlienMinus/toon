import re
from .exceptions import LexerError

TOKEN_SPEC = [
    ("HEADER", r"^@\w+"),
    ("KEY", r"[\w_]+"),
    ("COLON", r":"),
    ("SUBTOKEN", r"\w+\([^)]+\)"),
    ("WORD", r"[^\s]+"),
]


def tokenize_line(line: str):
    tokens = []
    pos = 0

    while pos < len(line):
        match = None
        for token_type, pattern in TOKEN_SPEC:
            regex = re.compile(pattern)
            match = regex.match(line, pos)
            if match:
                tokens.append((token_type, match.group()))
                pos = match.end()
                break

        if not match:
            if line[pos].isspace():
                pos += 1
            else:
                raise LexerError(f"Unexpected character: {line[pos]}")

    return tokens
