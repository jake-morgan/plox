from token.token import Token
from token.token import TokenType as tt


class Scanner:
    tokens = []
    start = 0
    current = 0
    line = 1

    def __init__(self, source):
        self.source = source

    def __is_at_end(self):
        """Determines if we are at the end of the file."""
        return self.current >= len(self.source)

    def scan_tokens(self):
        """Loops through source adding tokens to the token list."""
        while not self.__is_at_end():
            self.start = self.current
            self.__scan_token()

        self.tokens.append(Token(tt.EOF, "", None, self.line))
        return self.tokens

    def __scan_token(self):
        c = self.__advance()

        if c == "(":
            self.__add_token(tt.LEFT_PAREN)
        elif c == ")":
            self.__add_token(tt.RIGHT_PAREN)
        elif c == "{":
            self.__add_token(tt.LEFT_BRACE)
        elif c == "}":
            self.__add_token(tt.RIGHT_BRACE)
        elif c == ",":
            self.__add_token(tt.COMMA)
        elif c == ".":
            self.__add_token(tt.DOT)
        elif c == "-":
            self.__add_token(tt.MINUS)
        elif c == "+":
            self.__add_token(tt.PLUS)
        elif c == ";":
            self.__add_token(tt.SEMICOLON)
        elif c == "*":
            self.__add_token(tt.STAR)

    def __advance(self):
        self.current += 1
        return self.source[self.current - 1] # We need to return the character before we incremented

    def __add_token(self, token_type, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))
