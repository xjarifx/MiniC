"""
MiniC Semantic Analyzer
Performs semantic analysis including type checking and symbol table management.
"""

from typing import Dict, Optional, Set
from compiler.ast_nodes import *


class SemanticError(Exception):
    """Exception raised for semantic errors"""
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Semantic error at line {line}, column {column}: {message}")


class SymbolTable:
    """Symbol table for tracking variable declarations and types"""
    
    def __init__(self):
        self.symbols: Dict[str, str] = {}  # name -> type
        self.parent: Optional['SymbolTable'] = None
    
    def declare(self, name: str, var_type: str, line: int, column: int):
        """
        Declare a variable in this scope.
        
        Args:
            name: Variable name
            var_type: Variable type ('int' or 'bool')
            line: Line number for error reporting
            column: Column number for error reporting
            
        Raises:
            SemanticError: If variable already declared in this scope
        """
        if name in self.symbols:
            raise SemanticError(
                f"Variable '{name}' already declared in this scope",
                line,
                column
            )
        self.symbols[name] = var_type
    
    def lookup(self, name: str) -> Optional[str]:
        """
        Look up a variable's type in this scope or parent scopes.
        
        Args:
            name: Variable name
            
        Returns:
            Variable type or None if not found
        """
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None
    
    def enter_scope(self) -> 'SymbolTable':
        """Create a new nested scope"""
        new_scope = SymbolTable()
        new_scope.parent = self
        return new_scope
    
    def exit_scope(self) -> Optional['SymbolTable']:
        """Exit current scope and return to parent"""
        return self.parent


class SemanticAnalyzer(ASTVisitor):
    """
    Semantic analyzer for MiniC.
    
    Performs:
    - Variable declaration checking (no redeclarations)
    - Variable usage checking (all variables must be declared)
    - Type checking for expressions and assignments
    """
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_scope = self.symbol_table
        self.errors: list = []
    
    def analyze(self, ast: Program):
        """
        Perform semantic analysis on the AST.
        
        Args:
            ast: Root Program node
            
        Raises:
            SemanticError: If semantic errors are found
        """
        try:
            ast.accept(self)
        except SemanticError as e:
            self.errors.append(e)
        
        if self.errors:
            # Report all errors
            error_messages = [str(e) for e in self.errors]
            raise SemanticError(
                f"Found {len(self.errors)} semantic error(s):\n" + "\n".join(error_messages),
                0, 0
            )
    
    def visit_program(self, node: Program):
        """Visit program node"""
        for statement in node.statements:
            statement.accept(self)
    
    def visit_var_declaration(self, node: VarDeclaration):
        """Visit variable declaration node"""
        # Check for redeclaration
        self.current_scope.declare(node.name, node.var_type, node.line, node.column)
    
    def visit_assignment(self, node: Assignment):
        """Visit assignment node"""
        # Check if variable is declared
        var_type = self.current_scope.lookup(node.name)
        if var_type is None:
            raise SemanticError(
                f"Undeclared variable '{node.name}'",
                node.line,
                node.column
            )
        
        # Type check the expression
        expr_type = node.expression.accept(self)
        
        # Check type compatibility
        if var_type != expr_type:
            raise SemanticError(
                f"Type mismatch: cannot assign {expr_type} to {var_type} variable '{node.name}'",
                node.line,
                node.column
            )
    
    def visit_if_statement(self, node: IfStatement):
        """Visit if statement node"""
        # Check condition type (must be bool)
        cond_type = node.condition.accept(self)
        if cond_type != 'bool':
            raise SemanticError(
                f"If condition must be of type bool, got {cond_type}",
                node.line,
                node.column
            )
        
        # Enter new scope for then block
        self.current_scope = self.current_scope.enter_scope()
        for statement in node.then_block:
            statement.accept(self)
        self.current_scope = self.current_scope.exit_scope()
        
        # Enter new scope for else block (if exists)
        if node.else_block:
            self.current_scope = self.current_scope.enter_scope()
            for statement in node.else_block:
                statement.accept(self)
            self.current_scope = self.current_scope.exit_scope()
    
    def visit_while_statement(self, node: WhileStatement):
        """Visit while statement node"""
        # Check condition type (must be bool)
        cond_type = node.condition.accept(self)
        if cond_type != 'bool':
            raise SemanticError(
                f"While condition must be of type bool, got {cond_type}",
                node.line,
                node.column
            )
        
        # Enter new scope for loop body
        self.current_scope = self.current_scope.enter_scope()
        for statement in node.body:
            statement.accept(self)
        self.current_scope = self.current_scope.exit_scope()
    
    def visit_print_statement(self, node: PrintStatement):
        """Visit print statement node"""
        # Type check the expression (can be int or bool)
        node.expression.accept(self)
    
    def visit_block(self, node: Block):
        """Visit block node"""
        # Enter new scope
        self.current_scope = self.current_scope.enter_scope()
        for statement in node.statements:
            statement.accept(self)
        self.current_scope = self.current_scope.exit_scope()
    
    def visit_binary_op(self, node: BinaryOp) -> str:
        """
        Visit binary operation node and return result type.
        
        Returns:
            Result type of the operation
        """
        left_type = node.left.accept(self)
        right_type = node.right.accept(self)
        
        # Arithmetic operators: +, -, *, /, %
        if node.operator in ['+', '-', '*', '/', '%']:
            if left_type != 'int' or right_type != 'int':
                raise SemanticError(
                    f"Arithmetic operator '{node.operator}' requires int operands, got {left_type} and {right_type}",
                    node.line,
                    node.column
                )
            return 'int'
        
        # Comparison operators: <, >, <=, >=
        elif node.operator in ['<', '>', '<=', '>=']:
            if left_type != 'int' or right_type != 'int':
                raise SemanticError(
                    f"Comparison operator '{node.operator}' requires int operands, got {left_type} and {right_type}",
                    node.line,
                    node.column
                )
            return 'bool'
        
        # Equality operators: ==, !=
        elif node.operator in ['==', '!=']:
            if left_type != right_type:
                raise SemanticError(
                    f"Equality operator '{node.operator}' requires operands of same type, got {left_type} and {right_type}",
                    node.line,
                    node.column
                )
            return 'bool'
        
        # Logical operators: &&, ||
        elif node.operator in ['&&', '||']:
            if left_type != 'bool' or right_type != 'bool':
                raise SemanticError(
                    f"Logical operator '{node.operator}' requires bool operands, got {left_type} and {right_type}",
                    node.line,
                    node.column
                )
            return 'bool'
        
        else:
            raise SemanticError(
                f"Unknown operator '{node.operator}'",
                node.line,
                node.column
            )
    
    def visit_unary_op(self, node: UnaryOp) -> str:
        """
        Visit unary operation node and return result type.
        
        Returns:
            Result type of the operation
        """
        operand_type = node.operand.accept(self)
        
        # Negation: -
        if node.operator == '-':
            if operand_type != 'int':
                raise SemanticError(
                    f"Unary '-' requires int operand, got {operand_type}",
                    node.line,
                    node.column
                )
            return 'int'
        
        # Logical NOT: !
        elif node.operator == '!':
            if operand_type != 'bool':
                raise SemanticError(
                    f"Unary '!' requires bool operand, got {operand_type}",
                    node.line,
                    node.column
                )
            return 'bool'
        
        else:
            raise SemanticError(
                f"Unknown unary operator '{node.operator}'",
                node.line,
                node.column
            )
    
    def visit_identifier(self, node: Identifier) -> str:
        """
        Visit identifier node and return its type.
        
        Returns:
            Type of the variable
        """
        var_type = self.current_scope.lookup(node.name)
        if var_type is None:
            raise SemanticError(
                f"Undeclared variable '{node.name}'",
                node.line,
                node.column
            )
        return var_type
    
    def visit_int_literal(self, node: IntLiteral) -> str:
        """Visit integer literal node"""
        return 'int'
    
    def visit_bool_literal(self, node: BoolLiteral) -> str:
        """Visit boolean literal node"""
        return 'bool'


def analyze(ast: Program):
    """
    Convenience function to perform semantic analysis.
    
    Args:
        ast: Root Program node
        
    Raises:
        SemanticError: If semantic errors are found
    """
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)


def print_semantic_analysis(ast: Program) -> str:
    """
    Print semantic analysis results in tree format.
    
    Args:
        ast: Root Program node
        
    Returns:
        String representation of semantic analysis
    """
    analyzer = SemanticTreePrinter()
    try:
        return analyzer.print_analysis(ast)
    except SemanticError as e:
        return f"Semantic Error: {e}"


class SemanticTreePrinter(ASTVisitor):
    """Prints semantic analysis in tree format showing symbol tables and type checking"""
    
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_scope = self.symbol_table
        self.output = []
        self.indent_stack = []
        self.scope_counter = 0
    
    def print_analysis(self, ast: Program) -> str:
        """Perform analysis and return tree representation"""
        self.output = ["Semantic Analysis"]
        self.output.append("|-- Symbol Table (Global Scope)")
        ast.accept(self)
        
        # Print final symbol table
        if self.symbol_table.symbols:
            self.output.append("+-- Final Symbol Table:")
            symbols = list(self.symbol_table.symbols.items())
            for i, (name, var_type) in enumerate(symbols):
                is_last = (i == len(symbols) - 1)
                connector = "+-- " if is_last else "|-- "
                self.output.append(f"    {connector}{name}: {var_type}")
        
        return "\n".join(self.output)
    
    def _add_line(self, text: str, is_last: bool = False):
        """Add a line with proper indentation"""
        prefix = "".join(self.indent_stack)
        connector = "+-- " if is_last else "|-- "
        self.output.append(prefix + connector + text)
    
    def visit_program(self, node: Program):
        """Visit program node"""
        for i, statement in enumerate(node.statements):
            is_last = (i == len(node.statements) - 1)
            
            if is_last:
                self.indent_stack.append("    ")
            else:
                self.indent_stack.append("|   ")
            
            statement.accept(self)
            self.indent_stack.pop()
    
    def visit_var_declaration(self, node: VarDeclaration):
        """Visit variable declaration node"""
        self.current_scope.declare(node.name, node.var_type, node.line, node.column)
        self._add_line(f"VarDecl: {node.var_type} {node.name} [OK]")
    
    def visit_assignment(self, node: Assignment):
        """Visit assignment node"""
        var_type = self.current_scope.lookup(node.name)
        if var_type is None:
            self._add_line(f"Assignment: {node.name} = ??? [ERROR: Undeclared]")
            raise SemanticError(f"Undeclared variable '{node.name}'", node.line, node.column)
        
        expr_type = node.expression.accept(self)
        
        if var_type != expr_type:
            self._add_line(f"Assignment: {node.name} = ??? [ERROR: Type mismatch {expr_type} → {var_type}]")
            raise SemanticError(f"Type mismatch", node.line, node.column)
        
        self._add_line(f"Assignment: {node.name} = <{expr_type}> [OK]")
    
    def visit_if_statement(self, node: IfStatement):
        """Visit if statement node"""
        cond_type = node.condition.accept(self)
        
        if cond_type != 'bool':
            self._add_line(f"If [ERROR: Condition must be bool, got {cond_type}]")
            raise SemanticError(f"If condition must be bool", node.line, node.column)
        
        self._add_line(f"If: <{cond_type}> [OK]")
        
        # Then block - enter new scope
        self.scope_counter += 1
        scope_id = self.scope_counter
        self.indent_stack.append("|   " if node.else_block else "    ")
        self._add_line(f"Then (Scope {scope_id}):")
        self.indent_stack.pop()
        
        self.current_scope = self.current_scope.enter_scope()
        self.indent_stack.append("|   " if node.else_block else "    ")
        self.indent_stack.append("|   ")
        
        for i, statement in enumerate(node.then_block):
            is_last = (i == len(node.then_block) - 1)
            if is_last:
                self.indent_stack[-1] = "    "
            statement.accept(self)
        
        self.indent_stack.pop()
        self.indent_stack.pop()
        self.current_scope = self.current_scope.exit_scope()
        
        # Else block
        if node.else_block:
            self.scope_counter += 1
            scope_id = self.scope_counter
            self.indent_stack.append("    ")
            self._add_line(f"Else (Scope {scope_id}):", is_last=True)
            self.indent_stack.pop()
            
            self.current_scope = self.current_scope.enter_scope()
            self.indent_stack.append("    ")
            self.indent_stack.append("|   ")
            
            for i, statement in enumerate(node.else_block):
                is_last = (i == len(node.else_block) - 1)
                if is_last:
                    self.indent_stack[-1] = "    "
                statement.accept(self)
            
            self.indent_stack.pop()
            self.indent_stack.pop()
            self.current_scope = self.current_scope.exit_scope()
    
    def visit_while_statement(self, node: WhileStatement):
        """Visit while statement node"""
        cond_type = node.condition.accept(self)
        
        if cond_type != 'bool':
            self._add_line(f"While [ERROR: Condition must be bool, got {cond_type}]")
            raise SemanticError(f"While condition must be bool", node.line, node.column)
        
        self._add_line(f"While: <{cond_type}> [OK]")
        
        # Enter new scope for loop body
        self.scope_counter += 1
        scope_id = self.scope_counter
        self.indent_stack.append("    ")
        self._add_line(f"Body (Scope {scope_id}):")
        self.indent_stack.pop()
        
        self.current_scope = self.current_scope.enter_scope()
        self.indent_stack.append("    ")
        self.indent_stack.append("|   ")
        
        for i, statement in enumerate(node.body):
            is_last = (i == len(node.body) - 1)
            if is_last:
                self.indent_stack[-1] = "    "
            statement.accept(self)
        
        self.indent_stack.pop()
        self.indent_stack.pop()
        self.current_scope = self.current_scope.exit_scope()
    
    def visit_print_statement(self, node: PrintStatement):
        """Visit print statement node"""
        expr_type = node.expression.accept(self)
        self._add_line(f"Print: <{expr_type}> [OK]")
    
    def visit_block(self, node: Block):
        """Visit block node"""
        self.scope_counter += 1
        scope_id = self.scope_counter
        self._add_line(f"Block (Scope {scope_id}):")
        
        self.current_scope = self.current_scope.enter_scope()
        self.indent_stack.append("    ")
        self.indent_stack.append("|   ")
        
        for i, statement in enumerate(node.statements):
            is_last = (i == len(node.statements) - 1)
            if is_last:
                self.indent_stack[-1] = "    "
            statement.accept(self)
        
        self.indent_stack.pop()
        self.indent_stack.pop()
        self.current_scope = self.current_scope.exit_scope()
    
    def visit_binary_op(self, node: BinaryOp) -> str:
        """Visit binary operation node and return result type"""
        left_type = node.left.accept(self)
        right_type = node.right.accept(self)
        
        # Determine result type based on operator
        if node.operator in ['+', '-', '*', '/', '%']:
            if left_type != 'int' or right_type != 'int':
                raise SemanticError(f"Arithmetic operator requires int operands", node.line, node.column)
            return 'int'
        elif node.operator in ['<', '>', '<=', '>=']:
            if left_type != 'int' or right_type != 'int':
                raise SemanticError(f"Comparison operator requires int operands", node.line, node.column)
            return 'bool'
        elif node.operator in ['==', '!=']:
            if left_type != right_type:
                raise SemanticError(f"Equality operator requires same types", node.line, node.column)
            return 'bool'
        elif node.operator in ['&&', '||']:
            if left_type != 'bool' or right_type != 'bool':
                raise SemanticError(f"Logical operator requires bool operands", node.line, node.column)
            return 'bool'
        else:
            raise SemanticError(f"Unknown operator '{node.operator}'", node.line, node.column)
    
    def visit_unary_op(self, node: UnaryOp) -> str:
        """Visit unary operation node and return result type"""
        operand_type = node.operand.accept(self)
        
        if node.operator == '-':
            if operand_type != 'int':
                raise SemanticError(f"Unary '-' requires int operand", node.line, node.column)
            return 'int'
        elif node.operator == '!':
            if operand_type != 'bool':
                raise SemanticError(f"Unary '!' requires bool operand", node.line, node.column)
            return 'bool'
        else:
            raise SemanticError(f"Unknown unary operator", node.line, node.column)
    
    def visit_identifier(self, node: Identifier) -> str:
        """Visit identifier node and return its type"""
        var_type = self.current_scope.lookup(node.name)
        if var_type is None:
            raise SemanticError(f"Undeclared variable '{node.name}'", node.line, node.column)
        return var_type
    
    def visit_int_literal(self, node: IntLiteral) -> str:
        """Visit integer literal node"""
        return 'int'
    
    def visit_bool_literal(self, node: BoolLiteral) -> str:
        """Visit boolean literal node"""
        return 'bool'


# Testing
if __name__ == '__main__':
    from compiler.lexer import lex
    from compiler.parser import parse
    
    # Test 1: Valid program
    test_code_valid = """
    int x;
    int y;
    x = 10;
    y = x + 5;
    
    if (x < y) {
        print(x);
    }
    """
    
    # Test 2: Undeclared variable
    test_code_undeclared = """
    int x;
    x = y + 5;
    """
    
    # Test 3: Type mismatch
    test_code_type_mismatch = """
    int x;
    bool flag;
    x = flag;
    """
    
    # Test 4: Redeclaration
    test_code_redeclaration = """
    int x;
    int x;
    """
    
    tests = [
        ("Valid program", test_code_valid, True),
        ("Undeclared variable", test_code_undeclared, False),
        ("Type mismatch", test_code_type_mismatch, False),
        ("Redeclaration", test_code_redeclaration, False),
    ]
    
    for test_name, code, should_pass in tests:
        print(f"\nTest: {test_name}")
        try:
            tokens = lex(code)
            ast = parse(tokens)
            analyze(ast)
            if should_pass:
                print("[OK] Passed (as expected)")
            else:
                print("✗ Failed (expected error but passed)")
        except SemanticError as e:
            if not should_pass:
                print(f"[OK] Failed as expected: {e}")
            else:
                print(f"✗ Unexpected error: {e}")
        except Exception as e:
            print(f"✗ Unexpected exception: {e}")


