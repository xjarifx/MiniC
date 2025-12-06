"""
MiniC AST Node Definitions
Defines the Abstract Syntax Tree node classes.
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from abc import ABC, abstractmethod


class ASTNode(ABC):
    """Base class for all AST nodes"""
    
    @abstractmethod
    def accept(self, visitor):
        """Accept a visitor for the visitor pattern"""
        pass


# ============================================================================
# Statements
# ============================================================================

class Statement(ASTNode):
    """Base class for statement nodes"""
    pass


@dataclass
class Program(ASTNode):
    """Root node representing the entire program"""
    statements: List[Statement]
    
    def accept(self, visitor):
        return visitor.visit_program(self)
    
    def __repr__(self):
        return f"Program({len(self.statements)} statements)"


@dataclass
class VarDeclaration(Statement):
    """Variable declaration: int x; or bool flag;"""
    var_type: str  # 'int' or 'bool'
    name: str
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_var_declaration(self)
    
    def __repr__(self):
        return f"VarDecl({self.var_type} {self.name})"


@dataclass
class Assignment(Statement):
    """Assignment statement: x = expr;"""
    name: str
    expression: 'Expression'
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_assignment(self)
    
    def __repr__(self):
        return f"Assign({self.name} = {self.expression})"


@dataclass
class IfStatement(Statement):
    """If-else statement"""
    condition: 'Expression'
    then_block: List[Statement]
    else_block: Optional[List[Statement]]
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_if_statement(self)
    
    def __repr__(self):
        has_else = "with else" if self.else_block else "no else"
        return f"If({self.condition}, {has_else})"


@dataclass
class WhileStatement(Statement):
    """While loop statement"""
    condition: 'Expression'
    body: List[Statement]
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_while_statement(self)
    
    def __repr__(self):
        return f"While({self.condition})"


@dataclass
class PrintStatement(Statement):
    """Print statement: print(expr);"""
    expression: 'Expression'
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_print_statement(self)
    
    def __repr__(self):
        return f"Print({self.expression})"


@dataclass
class Block(Statement):
    """Block of statements enclosed in braces"""
    statements: List[Statement]
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_block(self)
    
    def __repr__(self):
        return f"Block({len(self.statements)} statements)"


# ============================================================================
# Expressions
# ============================================================================

class Expression(ASTNode):
    """Base class for expression nodes"""
    pass


@dataclass
class BinaryOp(Expression):
    """Binary operation: left op right"""
    operator: str  # +, -, *, /, %, <, >, <=, >=, ==, !=, &&, ||
    left: Expression
    right: Expression
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)
    
    def __repr__(self):
        return f"BinaryOp({self.left} {self.operator} {self.right})"


@dataclass
class UnaryOp(Expression):
    """Unary operation: op expr"""
    operator: str  # -, !
    operand: Expression
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)
    
    def __repr__(self):
        return f"UnaryOp({self.operator}{self.operand})"


@dataclass
class Identifier(Expression):
    """Variable reference"""
    name: str
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_identifier(self)
    
    def __repr__(self):
        return f"Id({self.name})"


@dataclass
class IntLiteral(Expression):
    """Integer literal"""
    value: int
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_int_literal(self)
    
    def __repr__(self):
        return f"Int({self.value})"


@dataclass
class BoolLiteral(Expression):
    """Boolean literal"""
    value: bool
    line: int
    column: int
    
    def accept(self, visitor):
        return visitor.visit_bool_literal(self)
    
    def __repr__(self):
        return f"Bool({self.value})"


# ============================================================================
# Visitor Interface (for traversing the AST)
# ============================================================================

class ASTVisitor(ABC):
    """Visitor interface for traversing and processing AST nodes"""
    
    @abstractmethod
    def visit_program(self, node: Program):
        pass
    
    @abstractmethod
    def visit_var_declaration(self, node: VarDeclaration):
        pass
    
    @abstractmethod
    def visit_assignment(self, node: Assignment):
        pass
    
    @abstractmethod
    def visit_if_statement(self, node: IfStatement):
        pass
    
    @abstractmethod
    def visit_while_statement(self, node: WhileStatement):
        pass
    
    @abstractmethod
    def visit_print_statement(self, node: PrintStatement):
        pass
    
    @abstractmethod
    def visit_block(self, node: Block):
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: BinaryOp):
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: UnaryOp):
        pass
    
    @abstractmethod
    def visit_identifier(self, node: Identifier):
        pass
    
    @abstractmethod
    def visit_int_literal(self, node: IntLiteral):
        pass
    
    @abstractmethod
    def visit_bool_literal(self, node: BoolLiteral):
        pass


# ============================================================================
# AST Pretty Printer (for debugging)
# ============================================================================

class ASTPrinter(ASTVisitor):
    """Prints AST in a human-readable tree format"""
    
    def __init__(self):
        self.indent_level = 0
    
    def _indent(self):
        return "  " * self.indent_level
    
    def visit_program(self, node: Program):
        result = [f"{self._indent()}Program:"]
        self.indent_level += 1
        for stmt in node.statements:
            result.append(stmt.accept(self))
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_var_declaration(self, node: VarDeclaration):
        return f"{self._indent()}VarDecl: {node.var_type} {node.name}"
    
    def visit_assignment(self, node: Assignment):
        result = [f"{self._indent()}Assignment: {node.name} ="]
        self.indent_level += 1
        result.append(node.expression.accept(self))
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_if_statement(self, node: IfStatement):
        result = [f"{self._indent()}If:"]
        self.indent_level += 1
        result.append(f"{self._indent()}Condition:")
        self.indent_level += 1
        result.append(node.condition.accept(self))
        self.indent_level -= 1
        result.append(f"{self._indent()}Then:")
        self.indent_level += 1
        for stmt in node.then_block:
            result.append(stmt.accept(self))
        self.indent_level -= 1
        if node.else_block:
            result.append(f"{self._indent()}Else:")
            self.indent_level += 1
            for stmt in node.else_block:
                result.append(stmt.accept(self))
            self.indent_level -= 1
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_while_statement(self, node: WhileStatement):
        result = [f"{self._indent()}While:"]
        self.indent_level += 1
        result.append(f"{self._indent()}Condition:")
        self.indent_level += 1
        result.append(node.condition.accept(self))
        self.indent_level -= 1
        result.append(f"{self._indent()}Body:")
        self.indent_level += 1
        for stmt in node.body:
            result.append(stmt.accept(self))
        self.indent_level -= 1
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_print_statement(self, node: PrintStatement):
        result = [f"{self._indent()}Print:"]
        self.indent_level += 1
        result.append(node.expression.accept(self))
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_block(self, node: Block):
        result = [f"{self._indent()}Block:"]
        self.indent_level += 1
        for stmt in node.statements:
            result.append(stmt.accept(self))
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_binary_op(self, node: BinaryOp):
        result = [f"{self._indent()}BinaryOp: {node.operator}"]
        self.indent_level += 1
        result.append(node.left.accept(self))
        result.append(node.right.accept(self))
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_unary_op(self, node: UnaryOp):
        result = [f"{self._indent()}UnaryOp: {node.operator}"]
        self.indent_level += 1
        result.append(node.operand.accept(self))
        self.indent_level -= 1
        return "\n".join(result)
    
    def visit_identifier(self, node: Identifier):
        return f"{self._indent()}Identifier: {node.name}"
    
    def visit_int_literal(self, node: IntLiteral):
        return f"{self._indent()}IntLiteral: {node.value}"
    
    def visit_bool_literal(self, node: BoolLiteral):
        return f"{self._indent()}BoolLiteral: {node.value}"


def print_ast(ast: ASTNode) -> str:
    """
    Pretty print an AST.
    
    Args:
        ast: Root AST node
        
    Returns:
        String representation of the AST
    """
    printer = ASTPrinter()
    return ast.accept(printer)
