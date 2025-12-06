"""
MiniC Lexer - Lexical Analyzer
Tokenizes MiniC source code into a stream of tokens.
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    """Token types for MiniC language"""
    # Keywords
    INT = auto()
    BOOL = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Identifiers and literals
    IDENTIFIER = auto()
    NUMBER = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    
    # Comparison operators
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    
    # Logical operators
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Assignment
    ASSIGN = auto()
    
    # Delimiters
    SEMICOLON = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    
    # Special
    EOF = auto()


@dataclass
class Token:
    """Represents a token with its type, value, and location"""
    type: TokenType
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', {self.line}:{self.column})"


class LexerError(Exception):
    """Exception raised for lexical errors"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Lexer error at line {line}, column {column}: {message}")


class Lexer:
    """
    Lexical analyzer for MiniC language.
    Converts source code into a stream of tokens.
    """
    
    # Keywords mapping
    KEYWORDS = {
        'int': TokenType.INT,
        'bool': TokenType.BOOL,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'print': TokenType.PRINT,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
    }
    
    # Token patterns (order matters!)
    TOKEN_PATTERNS = [
        # Skip multi-line comments
        (r'/\*.*?\*/', None),
        # Skip single-line comments
        (r'//[^\n]*', None),
        # Skip whitespace
        (r'[ \t\n\r]+', None),
        
        # Two-character operators (must come before single-character ones)
        (r'<=', TokenType.LESS_EQUAL),
        (r'>=', TokenType.GREATER_EQUAL),
        (r'==', TokenType.EQUAL),
        (r'!=', TokenType.NOT_EQUAL),
        (r'&&', TokenType.AND),
        (r'\|\|', TokenType.OR),
        
        # Single-character operators
        (r'\+', TokenType.PLUS),
        (r'-', TokenType.MINUS),
        (r'\*', TokenType.MULTIPLY),
        (r'/', TokenType.DIVIDE),
        (r'%', TokenType.MODULO),
        (r'<', TokenType.LESS_THAN),
        (r'>', TokenType.GREATER_THAN),
        (r'!', TokenType.NOT),
        (r'=', TokenType.ASSIGN),
        
        # Delimiters
        (r';', TokenType.SEMICOLON),
        (r'\(', TokenType.LPAREN),
        (r'\)', TokenType.RPAREN),
        (r'\{', TokenType.LBRACE),
        (r'\}', TokenType.RBRACE),
        
        # Identifiers (must come after keywords are checked)
        (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
        
        # Numbers
        (r'\d+', TokenType.NUMBER),
    ]
    
    def __init__(self, source_code: str):
        """
        Initialize the lexer with source code.
        
        Args:
            source_code: MiniC source code as a string
        """
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    def tokenize(self) -> List[Token]:
        """
        Tokenize the entire source code.
        
        Returns:
            List of tokens
            
        Raises:
            LexerError: If an invalid token is encountered
        """
        while self.position < len(self.source_code):
            self._next_token()
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return self.tokens
    
    def _next_token(self):
        """Extract the next token from the source code"""
        # Try to match each token pattern
        for pattern, token_type in self.TOKEN_PATTERNS:
            regex = re.compile(pattern, re.DOTALL)
            match = regex.match(self.source_code, self.position)
            
            if match:
                value = match.group(0)
                start_column = self.column
                
                # Skip tokens (comments, whitespace)
                if token_type is None:
                    self._advance(len(value))
                    return
                
                # Handle identifiers (could be keywords)
                if token_type == TokenType.IDENTIFIER:
                    if value in self.KEYWORDS:
                        token_type = self.KEYWORDS[value]
                
                # Create token
                token = Token(token_type, value, self.line, start_column)
                self.tokens.append(token)
                self._advance(len(value))
                return
        
        # No pattern matched - lexical error
        char = self.source_code[self.position]
        raise LexerError(f"Invalid character '{char}'", self.line, self.column)
    
    def _advance(self, count: int):
        """
        Advance position in source code and update line/column tracking.
        
        Args:
            count: Number of characters to advance
        """
        for _ in range(count):
            if self.position < len(self.source_code):
                if self.source_code[self.position] == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.position += 1


def lex(source_code: str) -> List[Token]:
    """
    Convenience function to tokenize source code.
    
    Args:
        source_code: MiniC source code as a string
        
    Returns:
        List of tokens
    """
    lexer = Lexer(source_code)
    return lexer.tokenize()


# Testing and debugging
if __name__ == '__main__':
    # Test code
    test_code = """
    // This is a test program
    int main() {
        int x;
        int y;
        x = 10;
        y = 20;
        
        /* Multi-line
           comment test */
        if (x < y) {
            print(x + y);
        }
        
        while (x < 100) {
            x = x * 2;
        }
    }
    """
    
    try:
        tokens = lex(test_code)
        print("Tokenization successful!")
        print(f"Total tokens: {len(tokens)}")
        print("\nTokens:")
        for token in tokens:
            print(f"  {token}")
    except LexerError as e:
        print(f"Error: {e}")
