class ToonError(Exception):
    """Base exception for TOON errors."""


class LexerError(ToonError):
    """Raised during tokenization."""


class ParserError(ToonError):
    """Raised during parsing."""
