"""
MiniC Parser - Syntax Analyzer
Parses tokens into an Abstract Syntax Tree (AST) using recursive descent.
"""

from typing import List, Optional
from compiler.lexer import Token, TokenType
from compiler.ast_nodes import *


class ParseError(Exception):
    """Exception raised for syntax errors"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Parse error at line {line}, column {column}: {message}")


class Parser:
    """
    Recursive descent parser for MiniC language.
    
    Grammar:
        program         → statement*
        statement       → varDecl | assignment | ifStmt | whileStmt | printStmt | block
        varDecl         → type IDENTIFIER ';'
        assignment      → IDENTIFIER '=' expression ';'
        ifStmt          → 'if' '(' expression ')' block ('else' block)?
        whileStmt       → 'while' '(' expression ')' block
        printStmt       → 'print' '(' expression ')' ';'
        block           → '{' statement* '}'
        
        expression      → logicalOr
        logicalOr       → logicalAnd ('||' logicalAnd)*
        logicalAnd      → equality ('&&' equality)*
        equality        → comparison (('==' | '!=') comparison)*
        comparison      → term (('<' | '>' | '<=' | '>=') term)*
        term            → factor (('+' | '-') factor)*
        factor          → unary (('*' | '/' | '%') unary)*
        unary           → ('!' | '-') unary | primary
        primary         → NUMBER | 'true' | 'false' | IDENTIFIER | '(' expression ')'
        
        type            → 'int' | 'bool'
    """
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize parser with tokens.
        
        Args:
            tokens: List of tokens from lexer
        """
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> Program:
        """
        Parse tokens into an AST.
        
        Returns:
            Program node (root of AST)
            
        Raises:
            ParseError: If syntax error is encountered
        """
        statements = []
        
        while not self._is_at_end():
            stmt = self._statement()
            if stmt:
                statements.append(stmt)
        
        return Program(statements)
    
    # ========================================================================
    # Statement parsing
    # ========================================================================
    
    def _statement(self) -> Optional[Statement]:
        """Parse a statement"""
        try:
            # Variable declaration
            if self._match(TokenType.INT, TokenType.BOOL):
                return self._var_declaration()
            
            # If statement
            if self._match(TokenType.IF):
                return self._if_statement()
            
            # While statement
            if self._match(TokenType.WHILE):
                return self._while_statement()
            
            # Print statement
            if self._match(TokenType.PRINT):
                return self._print_statement()
            
            # Block
            if self._check(TokenType.LBRACE):
                return self._block()
            
            # Assignment (must check identifier)
            if self._check(TokenType.IDENTIFIER):
                return self._assignment()
            
            # Unexpected token
            token = self._peek()
            raise ParseError(f"Unexpected token '{token.value}'", token.line, token.column)
            
        except ParseError:
            raise
    
    def _var_declaration(self) -> VarDeclaration:
        """Parse variable declaration: type IDENTIFIER ';'"""
        type_token = self._previous()
        var_type = type_token.value
        
        name_token = self._consume(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value
        
        self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        
        return VarDeclaration(var_type, name, type_token.line, type_token.column)
    
    def _assignment(self) -> Assignment:
        """Parse assignment: IDENTIFIER '=' expression ';'"""
        name_token = self._consume(TokenType.IDENTIFIER, "Expected variable name")
        name = name_token.value
        
        self._consume(TokenType.ASSIGN, "Expected '=' in assignment")
        
        expression = self._expression()
        
        self._consume(TokenType.SEMICOLON, "Expected ';' after assignment")
        
        return Assignment(name, expression, name_token.line, name_token.column)
    
    def _if_statement(self) -> IfStatement:
        """Parse if statement: 'if' '(' expression ')' block ('else' block)?"""
        if_token = self._previous()
        
        self._consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after if condition")
        
        then_block = self._block()
        else_block = None
        
        if self._match(TokenType.ELSE):
            else_block = self._block()
        
        return IfStatement(
            condition,
            then_block.statements if isinstance(then_block, Block) else [then_block],
            else_block.statements if else_block and isinstance(else_block, Block) else ([] if else_block is None else [else_block]),
            if_token.line,
            if_token.column
        )
    
    def _while_statement(self) -> WhileStatement:
        """Parse while statement: 'while' '(' expression ')' block"""
        while_token = self._previous()
        
        self._consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after while condition")
        
        body = self._block()
        
        return WhileStatement(
            condition,
            body.statements if isinstance(body, Block) else [body],
            while_token.line,
            while_token.column
        )
    
    def _print_statement(self) -> PrintStatement:
        """Parse print statement: 'print' '(' expression ')' ';'"""
        print_token = self._previous()
        
        self._consume(TokenType.LPAREN, "Expected '(' after 'print'")
        expression = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after print expression")
        self._consume(TokenType.SEMICOLON, "Expected ';' after print statement")
        
        return PrintStatement(expression, print_token.line, print_token.column)
    
    def _block(self) -> Block:
        """Parse block: '{' statement* '}'"""
        open_brace = self._consume(TokenType.LBRACE, "Expected '{'")
        
        statements = []
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            stmt = self._statement()
            if stmt:
                statements.append(stmt)
        
        self._consume(TokenType.RBRACE, "Expected '}' after block")
        
        return Block(statements, open_brace.line, open_brace.column)
    
    # ========================================================================
    # Expression parsing (precedence climbing)
    # ========================================================================
    
    def _expression(self) -> Expression:
        """Parse expression"""
        return self._logical_or()
    
    def _logical_or(self) -> Expression:
        """Parse logical OR: logicalAnd ('||' logicalAnd)*"""
        expr = self._logical_and()
        
        while self._match(TokenType.OR):
            operator = self._previous()
            right = self._logical_and()
            expr = BinaryOp('||', expr, right, operator.line, operator.column)
        
        return expr
    
    def _logical_and(self) -> Expression:
        """Parse logical AND: equality ('&&' equality)*"""
        expr = self._equality()
        
        while self._match(TokenType.AND):
            operator = self._previous()
            right = self._equality()
            expr = BinaryOp('&&', expr, right, operator.line, operator.column)
        
        return expr
    
    def _equality(self) -> Expression:
        """Parse equality: comparison (('==' | '!=') comparison)*"""
        expr = self._comparison()
        
        while self._match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            operator = self._previous()
            op_str = '==' if operator.type == TokenType.EQUAL else '!='
            right = self._comparison()
            expr = BinaryOp(op_str, expr, right, operator.line, operator.column)
        
        return expr
    
    def _comparison(self) -> Expression:
        """Parse comparison: term (('<' | '>' | '<=' | '>=') term)*"""
        expr = self._term()
        
        while self._match(TokenType.LESS_THAN, TokenType.GREATER_THAN, 
                          TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            operator = self._previous()
            op_map = {
                TokenType.LESS_THAN: '<',
                TokenType.GREATER_THAN: '>',
                TokenType.LESS_EQUAL: '<=',
                TokenType.GREATER_EQUAL: '>='
            }
            op_str = op_map[operator.type]
            right = self._term()
            expr = BinaryOp(op_str, expr, right, operator.line, operator.column)
        
        return expr
    
    def _term(self) -> Expression:
        """Parse term: factor (('+' | '-') factor)*"""
        expr = self._factor()
        
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            op_str = '+' if operator.type == TokenType.PLUS else '-'
            right = self._factor()
            expr = BinaryOp(op_str, expr, right, operator.line, operator.column)
        
        return expr
    
    def _factor(self) -> Expression:
        """Parse factor: unary (('*' | '/' | '%') unary)*"""
        expr = self._unary()
        
        while self._match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            operator = self._previous()
            op_map = {
                TokenType.MULTIPLY: '*',
                TokenType.DIVIDE: '/',
                TokenType.MODULO: '%'
            }
            op_str = op_map[operator.type]
            right = self._unary()
            expr = BinaryOp(op_str, expr, right, operator.line, operator.column)
        
        return expr
    
    def _unary(self) -> Expression:
        """Parse unary: ('!' | '-') unary | primary"""
        if self._match(TokenType.NOT, TokenType.MINUS):
            operator = self._previous()
            op_str = '!' if operator.type == TokenType.NOT else '-'
            operand = self._unary()
            return UnaryOp(op_str, operand, operator.line, operator.column)
        
        return self._primary()
    
    def _primary(self) -> Expression:
        """Parse primary: NUMBER | 'true' | 'false' | IDENTIFIER | '(' expression ')'"""
        # Boolean literals
        if self._match(TokenType.TRUE):
            token = self._previous()
            return BoolLiteral(True, token.line, token.column)
        
        if self._match(TokenType.FALSE):
            token = self._previous()
            return BoolLiteral(False, token.line, token.column)
        
        # Number literal
        if self._match(TokenType.NUMBER):
            token = self._previous()
            return IntLiteral(int(token.value), token.line, token.column)
        
        # Identifier
        if self._match(TokenType.IDENTIFIER):
            token = self._previous()
            return Identifier(token.value, token.line, token.column)
        
        # Parenthesized expression
        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        # Error
        token = self._peek()
        raise ParseError(f"Expected expression, got '{token.value}'", token.line, token.column)
    
    # ========================================================================
    # Helper methods
    # ========================================================================
    
    def _match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False
    
    def _check(self, token_type: TokenType) -> bool:
        """Check if current token is of given type"""
        if self._is_at_end():
            return False
        return self._peek().type == token_type
    
    def _advance(self) -> Token:
        """Consume current token and return it"""
        if not self._is_at_end():
            self.current += 1
        return self._previous()
    
    def _is_at_end(self) -> bool:
        """Check if at end of tokens"""
        return self._peek().type == TokenType.EOF
    
    def _peek(self) -> Token:
        """Get current token without consuming it"""
        return self.tokens[self.current]
    
    def _previous(self) -> Token:
        """Get previous token"""
        return self.tokens[self.current - 1]
    
    def _consume(self, token_type: TokenType, message: str) -> Token:
        """Consume token of expected type or raise error"""
        if self._check(token_type):
            return self._advance()
        
        token = self._peek()
        raise ParseError(message, token.line, token.column)


def parse(tokens: List[Token]) -> Program:
    """
    Convenience function to parse tokens into AST.
    
    Args:
        tokens: List of tokens from lexer
        
    Returns:
        Program node (root of AST)
    """
    parser = Parser(tokens)
    return parser.parse()


# Testing
if __name__ == '__main__':
    from compiler.lexer import lex
    from compiler.ast_nodes import print_ast
    
    test_code = """
    int x;
    int y;
    x = 10;
    y = 20;
    
    if (x < y) {
        print(x + y);
    }
    
    while (x < 100) {
        x = x * 2;
    }
    """
    
    try:
        tokens = lex(test_code)
        ast = parse(tokens)
        print("Parsing successful!")
        print("\nAST:")
        print(print_ast(ast))
    except (ParseError, Exception) as e:
        print(f"Error: {e}")
