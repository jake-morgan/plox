# pylint: disable=import-error, no-name-in-module, no-member

from token.token import Token
from token.token import TokenType as tt

import plox


class Scanner:
    tokens = []
    start = 0
    current = 0
    line = 1

    # Language reserved keywords
    keywords = {
        "and": tt.AND,
        "class": tt.CLASS,
        "else": tt.ELSE,
        "false": tt.FALSE,
        "for": tt.FOR,
        "fun": tt.FUN,
        "if": tt.IF,
        "nil": tt.NIL,
        "or": tt.OR,
        "print": tt.PRINT,
        "return": tt.RETURN,
        "super": tt.SUPER,
        "this": tt.THIS,
        "true": tt.TRUE,
        "var": tt.VAR,
        "while": tt.WHILE,
    }

    def __init__(self, source):
        self.source = source

    def _is_at_end(self):
        """Determines if we are at the end of the file."""
        return self.current >= len(self.source)

    def scan_tokens(self):
        """Loops through source adding tokens to the token list."""
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()

        self.tokens.append(Token(tt.EOF, "", None, self.line))
        return self.tokens

    # pylint: disable=too-many-branches, too-many-statements
    def _scan_token(self):
        c = self._advance()

        # Single tokens
        if c == "(":
            self._add_token(tt.LEFT_PAREN)
        elif c == ")":
            self._add_token(tt.RIGHT_PAREN)
        elif c == "{":
            self._add_token(tt.LEFT_BRACE)
        elif c == "}":
            self._add_token(tt.RIGHT_BRACE)
        elif c == ",":
            self._add_token(tt.COMMA)
        elif c == ".":
            self._add_token(tt.DOT)
        elif c == "-":
            self._add_token(tt.MINUS)
        elif c == "+":
            self._add_token(tt.PLUS)
        elif c == ";":
            self._add_token(tt.SEMICOLON)
        elif c == "*":
            self._add_token(tt.STAR)
        # Single or double tokens
        elif c == "!":
            if self._match("=") is True:
                self._add_token(tt.BANG_EQUAL)
            else:
                self._add_token(tt.BANG)
        elif c == "=":
            if self._match("=") is True:
                self._add_token(tt.EQUAL_EQUAL)
            else:
                self._add_token(tt.EQUAL)
        elif c == "<":
            if self._match("=") is True:
                self._add_token(tt.LESS_EQUAL)
            else:
                self._add_token(tt.LESS)
        elif c == ">":
            if self._match("=") is True:
                self._add_token(tt.GREATER_EQUAL)
            else:
                self._add_token(tt.GREATER)
        elif c == "/":
            if self._match("/") is True:
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(tt.SLASH)
        # Whitespace
        elif c in [" ", "\r", "\t"]:
            pass
        elif c == "\n":
            self.line += 1
        # Literals
        elif c == '"':
            self._string()
        elif self._is_digit(c) is True:
            self._number()
        # Reserved keywords
        elif self._is_alpha(c):
            self._identifier()
        # Unrecognised token
        else:
            plox.error(self.line, f'Unexpected c "{c}".')

    def _advance(self):
        self.current += 1
        return self.source[
            self.current - 1
        ]  # We need to return the character from before we incremented.

    def _peek(self):
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _match(self, expected):
        if self._is_at_end() is True:
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def _is_digit(self, c):
        return c >= "0" and c <= "9"

    def _is_alpha(self, c):
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or (c == "_")

    def _is_alpha_numeric(self, c):
        return self._is_alpha(c) or self._is_digit(c)

    def _add_token(self, token_type, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def _string(self):
        while self._peek() != '"' and self._is_at_end() is False:
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        if self._is_at_end() is True:
            plox.error(self.line, "Unterminated string.")
            return

        # The closing ".
        self._advance()

        # Trim the surrounding quotes
        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(tt.STRING, value)

    def _number(self):
        while self._is_digit(self._peek()):
            self._advance()

        # Check for decimal
        if self._peek() == "." and self._is_digit(self._peek_next()):
            # Move over the "."
            self._advance()
            # Continue advancing over the decimal
            while self._is_digit(self._peek()):
                self._advance()

        self._add_token(tt.NUMBER, float(self.source[self.start : self.current]))

    def _identifier(self):
        while self._is_alpha_numeric(self._peek()):
            self._advance()

        text = self.source[self.start : self.current]
        self._add_token(self.keywords.get(text, tt.IDENTIFIER))
