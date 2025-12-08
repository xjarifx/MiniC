"""
MiniC IR Generator
Generates Three-Address Code (TAC) intermediate representation.
"""

from typing import List, Optional
from dataclasses import dataclass
from compiler.ast_nodes import *


@dataclass
class TACInstruction:
    """Base class for TAC instructions"""
    pass


@dataclass
class TACAssign(TACInstruction):
    """Assignment: dest = src"""
    dest: str
    src: str
    
    def __repr__(self):
        return f"{self.dest} = {self.src}"


@dataclass
class TACBinaryOp(TACInstruction):
    """Binary operation: dest = left op right"""
    dest: str
    left: str
    op: str
    right: str
    
    def __repr__(self):
        return f"{self.dest} = {self.left} {self.op} {self.right}"


@dataclass
class TACUnaryOp(TACInstruction):
    """Unary operation: dest = op operand"""
    dest: str
    op: str
    operand: str
    
    def __repr__(self):
        return f"{self.dest} = {self.op}{self.operand}"


@dataclass
class TACLabel(TACInstruction):
    """Label: label:"""
    label: str
    
    def __repr__(self):
        return f"{self.label}:"


@dataclass
class TACGoto(TACInstruction):
    """Unconditional jump: goto label"""
    label: str
    
    def __repr__(self):
        return f"goto {self.label}"


@dataclass
class TACIfFalse(TACInstruction):
    """Conditional jump: if !condition goto label"""
    condition: str
    label: str
    
    def __repr__(self):
        return f"if !{self.condition} goto {self.label}"


@dataclass
class TACPrint(TACInstruction):
    """Print statement: print value"""
    value: str
    
    def __repr__(self):
        return f"print {self.value}"


@dataclass
class TACVarDecl(TACInstruction):
    """Variable declaration: var type name"""
    var_type: str
    name: str
    
    def __repr__(self):
        return f"var {self.var_type} {self.name}"


class IRGenerator(ASTVisitor):
    """
    Generates Three-Address Code (TAC) from AST.
    
    TAC characteristics:
    - Each instruction has at most one operator
    - Each instruction has at most three operands
    - Temporary variables for intermediate results
    - Labels for control flow
    """
    
    def __init__(self):
        self.instructions: List[TACInstruction] = []
        self.temp_count = 0
        self.label_count = 0
    
    def generate(self, ast: Program) -> List[TACInstruction]:
        """
        Generate TAC from AST.
        
        Args:
            ast: Root Program node
            
        Returns:
            List of TAC instructions
        """
        ast.accept(self)
        return self.instructions
    
    def new_temp(self) -> str:
        """Generate a new temporary variable name"""
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def new_label(self) -> str:
        """Generate a new label name"""
        label = f"L{self.label_count}"
        self.label_count += 1
        return label
    
    def visit_program(self, node: Program):
        """Visit program node"""
        for statement in node.statements:
            statement.accept(self)
    
    def visit_var_declaration(self, node: VarDeclaration):
        """Visit variable declaration node"""
        self.instructions.append(TACVarDecl(node.var_type, node.name))
    
    def visit_assignment(self, node: Assignment) -> Optional[str]:
        """Visit assignment node - INEFFICIENT VERSION"""
        # Generate code for expression
        expr_result = node.expression.accept(self)
        
        # INEFFICIENCY 1: Create unnecessary temporary
        temp = self.new_temp()
        self.instructions.append(TACAssign(temp, expr_result))
        
        # INEFFICIENCY 2: Create another unnecessary temporary
        temp2 = self.new_temp()
        self.instructions.append(TACAssign(temp2, temp))
        
        # Generate assignment from second temp
        self.instructions.append(TACAssign(node.name, temp2))
        
        return None
    
    def visit_if_statement(self, node: IfStatement) -> Optional[str]:
        """
        Visit if statement node - INEFFICIENT VERSION
        
        Generated code:
            [condition code]
            if !condition goto else_label
            [then block]
            goto end_label
            else_label:
            [else block]
            end_label:
        """
        # Generate code for condition
        cond_result = node.condition.accept(self)
        
        # INEFFICIENCY 1: Create unnecessary temps for condition
        temp1 = self.new_temp()
        self.instructions.append(TACAssign(temp1, cond_result))
        
        temp2 = self.new_temp()
        self.instructions.append(TACAssign(temp2, temp1))
        
        # Create labels
        else_label = self.new_label()
        end_label = self.new_label()
        
        # If condition is false, jump to else
        self.instructions.append(TACIfFalse(temp2, else_label))
        
        # Then block
        for statement in node.then_block:
            statement.accept(self)
        
        # Jump to end
        self.instructions.append(TACGoto(end_label))
        
        # Else label
        self.instructions.append(TACLabel(else_label))
        
        # Else block (if exists)
        if node.else_block:
            for statement in node.else_block:
                statement.accept(self)
        
        # End label
        self.instructions.append(TACLabel(end_label))
        
        return None
    
    def visit_while_statement(self, node: WhileStatement) -> Optional[str]:
        """
        Visit while statement node - INEFFICIENT VERSION
        
        Generated code:
            start_label:
            [condition code]
            if !condition goto end_label
            [body]
            goto start_label
            end_label:
        """
        # Create labels
        start_label = self.new_label()
        end_label = self.new_label()
        
        # Start label
        self.instructions.append(TACLabel(start_label))
        
        # Generate code for condition
        cond_result = node.condition.accept(self)
        
        # INEFFICIENCY: Create unnecessary temps for condition
        temp1 = self.new_temp()
        self.instructions.append(TACAssign(temp1, cond_result))
        
        temp2 = self.new_temp()
        self.instructions.append(TACAssign(temp2, temp1))
        
        # If condition is false, exit loop
        self.instructions.append(TACIfFalse(temp2, end_label))
        
        # Loop body
        for statement in node.body:
            statement.accept(self)
        
        # Jump back to start
        self.instructions.append(TACGoto(start_label))
        
        # End label
        self.instructions.append(TACLabel(end_label))
        
        return None
    
    def visit_print_statement(self, node: PrintStatement) -> Optional[str]:
        """Visit print statement node - INEFFICIENT VERSION"""
        # Generate code for expression
        expr_result = node.expression.accept(self)
        
        # INEFFICIENCY: Create unnecessary temps before printing
        temp1 = self.new_temp()
        self.instructions.append(TACAssign(temp1, expr_result))
        
        temp2 = self.new_temp()
        self.instructions.append(TACAssign(temp2, temp1))
        
        # Generate print instruction
        self.instructions.append(TACPrint(temp2))
        
        return None
    
    def visit_block(self, node: Block) -> Optional[str]:
        """Visit block node"""
        for statement in node.statements:
            statement.accept(self)
        return None
    
    def visit_binary_op(self, node: BinaryOp) -> str:
        """
        Visit binary operation node and return temp holding result.
        INEFFICIENT VERSION - Creates unnecessary temporaries
        
        Returns:
            Name of temporary variable holding result
        """
        # Generate code for operands
        left_result = node.left.accept(self)
        right_result = node.right.accept(self)
        
        # INEFFICIENCY 1: Create unnecessary temps to copy operands
        left_temp = self.new_temp()
        self.instructions.append(TACAssign(left_temp, left_result))
        
        right_temp = self.new_temp()
        self.instructions.append(TACAssign(right_temp, right_result))
        
        # Create temporary for result
        result_temp = self.new_temp()
        
        # Generate binary operation using the copied temps
        self.instructions.append(TACBinaryOp(result_temp, left_temp, node.operator, right_temp))
        
        # INEFFICIENCY 2: Copy result to another temp
        final_temp = self.new_temp()
        self.instructions.append(TACAssign(final_temp, result_temp))
        
        return final_temp
    
    def visit_unary_op(self, node: UnaryOp) -> str:
        """
        Visit unary operation node and return temp holding result.
        INEFFICIENT VERSION - Creates unnecessary temporaries
        
        Returns:
            Name of temporary variable holding result
        """
        # Generate code for operand
        operand_result = node.operand.accept(self)
        
        # INEFFICIENCY 1: Create unnecessary temp to copy operand
        operand_temp = self.new_temp()
        self.instructions.append(TACAssign(operand_temp, operand_result))
        
        # Create temporary for result
        result_temp = self.new_temp()
        
        # Generate unary operation using the copied temp
        self.instructions.append(TACUnaryOp(result_temp, node.operator, operand_temp))
        
        # INEFFICIENCY 2: Copy result to another temp
        final_temp = self.new_temp()
        self.instructions.append(TACAssign(final_temp, result_temp))
        
        return final_temp
    
    def visit_identifier(self, node: Identifier) -> str:
        """
        Visit identifier node and return variable name.
        
        Returns:
            Variable name
        """
        return node.name
    
    def visit_int_literal(self, node: IntLiteral) -> str:
        """
        Visit integer literal node and return string representation.
        
        Returns:
            String representation of the integer
        """
        return str(node.value)
    
    def visit_bool_literal(self, node: BoolLiteral) -> str:
        """
        Visit boolean literal node and return string representation.
        
        Returns:
            String representation of the boolean
        """
        return 'true' if node.value else 'false'


def generate_ir(ast: Program) -> List[TACInstruction]:
    """
    Convenience function to generate TAC from AST.
    
    Args:
        ast: Root Program node
        
    Returns:
        List of TAC instructions
    """
    generator = IRGenerator()
    return generator.generate(ast)


def print_ir(instructions: List[TACInstruction]) -> str:
    """
    Pretty print TAC instructions.
    
    Args:
        instructions: List of TAC instructions
        
    Returns:
        String representation of TAC
    """
    lines = []
    for instr in instructions:
        # Indent labels less than regular instructions
        if isinstance(instr, TACLabel):
            lines.append(str(instr))
        else:
            lines.append(f"    {instr}")
    return "\n".join(lines)


# Testing
if __name__ == '__main__':
    from compiler.lexer import lex
    from compiler.parser import parse
    from compiler.semantic import analyze
    
    test_code = """
    int x;
    int y;
    int result;
    
    x = 10;
    y = 20;
    
    if (x < y) {
        result = x + y;
        print(result);
    } else {
        result = x - y;
        print(result);
    }
    
    while (x < 100) {
        x = x * 2;
        print(x);
    }
    """
    
    try:
        print("Compiling to IR...")
        tokens = lex(test_code)
        ast = parse(tokens)
        analyze(ast)
        ir = generate_ir(ast)
        
        print("\nThree-Address Code (TAC):")
        print("=" * 50)
        print(print_ir(ir))
        print("=" * 50)
        print(f"\nTotal instructions: {len(ir)}")
        
    except Exception as e:
        print(f"Error: {e}")
