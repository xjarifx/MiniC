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
    """Prints AST in traditional syntax tree format with terminals as leaves"""
    
    def __init__(self):
        self.indent_level = 0
        self.prefixes = []
    
    def _format_tree(self, node_label: str, children: list) -> list:
        """Format a node with its children"""
        lines = [node_label]
        
        for i, child in enumerate(children):
            is_last = (i == len(children) - 1)
            connector = "+-- " if is_last else "|-- "
            extension = "    " if is_last else "|   "
            
            if isinstance(child, str):
                # Simple string child (terminal)
                lines.append(connector + child)
            elif isinstance(child, list):
                # List of lines from child node
                lines.append(connector + child[0])
                for subline in child[1:]:
                    lines.append(extension + subline)
        
        return lines
    
    def visit_program(self, node: Program):
        """Program node (root) with statement children"""
        children = [stmt.accept(self) for stmt in node.statements]
        lines = self._format_tree("<Program>", children)
        return "\n".join(lines)
    
    def visit_var_declaration(self, node: VarDeclaration):
        """Variable declaration node with type and identifier as leaves"""
        return self._format_tree(
            "<VarDeclaration>",
            [
                f"<Type>: {node.var_type}",
                f"<Identifier>: {node.name}"
            ]
        )
    
    def visit_assignment(self, node: Assignment):
        """Assignment statement with identifier and expression"""
        expr_tree = node.expression.accept(self)
        return self._format_tree(
            "<Assignment>",
            [
                f"<Identifier>: {node.name}",
                f"<Operator>: =",
                expr_tree
            ]
        )
    
    def visit_if_statement(self, node: IfStatement):
        """If statement with condition, then block, and optional else block"""
        cond_tree = node.condition.accept(self)
        then_stmts = [stmt.accept(self) for stmt in node.then_block]
        then_tree = self._format_tree("<ThenBlock>", then_stmts)
        
        children = [cond_tree, then_tree]
        
        if node.else_block:
            else_stmts = [stmt.accept(self) for stmt in node.else_block]
            else_tree = self._format_tree("<ElseBlock>", else_stmts)
            children.append(else_tree)
        
        return self._format_tree("<IfStatement>", children)
    
    def visit_while_statement(self, node: WhileStatement):
        """While statement with condition and body"""
        cond_tree = node.condition.accept(self)
        body_stmts = [stmt.accept(self) for stmt in node.body]
        body_tree = self._format_tree("<Body>", body_stmts)
        
        return self._format_tree("<WhileStatement>", [cond_tree, body_tree])
    
    def visit_print_statement(self, node: PrintStatement):
        """Print statement with expression"""
        expr_tree = node.expression.accept(self)
        return self._format_tree("<PrintStatement>", [expr_tree])
    
    def visit_block(self, node: Block):
        """Block statement containing multiple statements"""
        stmt_trees = [stmt.accept(self) for stmt in node.statements]
        return self._format_tree("<Block>", stmt_trees)
    
    def visit_binary_op(self, node: BinaryOp):
        """Binary operation with operator and two operands"""
        left_tree = node.left.accept(self)
        right_tree = node.right.accept(self)
        
        return self._format_tree(
            "<BinaryExpression>",
            [
                left_tree,
                f"<Operator>: {node.operator}",
                right_tree
            ]
        )
    
    def visit_unary_op(self, node: UnaryOp):
        """Unary operation with operator and operand"""
        operand_tree = node.operand.accept(self)
        
        return self._format_tree(
            "<UnaryExpression>",
            [
                f"<Operator>: {node.operator}",
                operand_tree
            ]
        )
    
    def visit_identifier(self, node: Identifier):
        """Identifier leaf node (terminal)"""
        return [f"<Identifier>: {node.name}"]
    
    def visit_int_literal(self, node: IntLiteral):
        """Integer literal leaf node (terminal)"""
        return [f"<IntLiteral>: {node.value}"]
    
    def visit_bool_literal(self, node: BoolLiteral):
        """Boolean literal leaf node (terminal)"""
        return [f"<BoolLiteral>: {node.value}"]


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
