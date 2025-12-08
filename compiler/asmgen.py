"""
MiniC Assembly Generator
Generates readable pseudocode assembly from IR.
"""

from typing import List, Dict
from compiler.ir_generator import *


class AssemblyGenerator:
    """
    Generates readable pseudocode assembly from Three-Address Code.
    This is human-readable and shows the flow of execution.
    """
    
    def __init__(self):
        self.asm_lines: List[str] = []
        self.variables: set = set()  # Track all variables
        self.indent_level = 1
    
    def generate(self, instructions: List[TACInstruction]) -> str:
        """
        Generate readable pseudocode assembly from TAC instructions.
        
        Args:
            instructions: List of TAC instructions
            
        Returns:
            Pseudocode assembly as string
        """
        self.asm_lines = []
        self.variables = set()
        
        # Collect all variables
        for instr in instructions:
            if isinstance(instr, TACVarDecl):
                self.variables.add(instr.name)
            elif isinstance(instr, TACAssign):
                if not self._is_constant(instr.dest):
                    self.variables.add(instr.dest)
            elif isinstance(instr, TACBinaryOp):
                self.variables.add(instr.dest)
            elif isinstance(instr, TACUnaryOp):
                self.variables.add(instr.dest)
        
        # Header
        self.asm_lines.append("=" * 70)
        self.asm_lines.append("PSEUDOCODE ASSEMBLY")
        self.asm_lines.append("=" * 70)
        self.asm_lines.append("")
        self.asm_lines.append("PROGRAM START:")
        self.asm_lines.append("")
        
        # Variable declarations
        if self.variables:
            self.asm_lines.append("  // Allocate memory for variables")
            for var in sorted(self.variables):
                self.asm_lines.append(f"  DECLARE {var}")
            self.asm_lines.append("")
        
        # Generate code for each instruction
        for instr in instructions:
            self._generate_instruction(instr)
        
        # Footer
        self.asm_lines.append("")
        self.asm_lines.append("  RETURN 0")
        self.asm_lines.append("")
        self.asm_lines.append("PROGRAM END")
        self.asm_lines.append("=" * 70)
        
        return "\n".join(self.asm_lines) + "\n"
    
    def _generate_instruction(self, instr: TACInstruction):
        """Generate pseudocode assembly for a single TAC instruction"""
        indent = "  "
        
        if isinstance(instr, TACVarDecl):
            # Variable declarations are handled in the header
            pass
        
        elif isinstance(instr, TACAssign):
            # dest = src
            self.asm_lines.append(f"{indent}SET {instr.dest} = {instr.src}")
        
        elif isinstance(instr, TACBinaryOp):
            # dest = left op right
            op_name = {
                '+': 'ADD',
                '-': 'SUBTRACT',
                '*': 'MULTIPLY',
                '/': 'DIVIDE',
                '%': 'MODULO',
                '<': 'LESS_THAN',
                '>': 'GREATER_THAN',
                '<=': 'LESS_EQUAL',
                '>=': 'GREATER_EQUAL',
                '==': 'EQUALS',
                '!=': 'NOT_EQUALS',
                '&&': 'AND',
                '||': 'OR'
            }.get(instr.op, instr.op)
            
            self.asm_lines.append(f"{indent}SET {instr.dest} = {op_name}({instr.left}, {instr.right})")
        
        elif isinstance(instr, TACUnaryOp):
            # dest = op operand
            op_name = {
                '-': 'NEGATE',
                '!': 'NOT'
            }.get(instr.op, instr.op)
            
            self.asm_lines.append(f"{indent}SET {instr.dest} = {op_name}({instr.operand})")
        
        elif isinstance(instr, TACLabel):
            # Label
            self.asm_lines.append(f"\n{instr.label}:")
        
        elif isinstance(instr, TACGoto):
            # Unconditional jump
            self.asm_lines.append(f"{indent}GOTO {instr.label}")
        
        elif isinstance(instr, TACIfFalse):
            # Conditional jump
            self.asm_lines.append(f"{indent}IF {instr.condition} == false THEN GOTO {instr.label}")
        
        elif isinstance(instr, TACPrint):
            # Print statement
            self.asm_lines.append(f"{indent}PRINT({instr.value})")
    
    def _is_constant(self, value: str) -> bool:
        """Check if value is a constant literal"""
        if value in ['true', 'false']:
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False


def generate_assembly(instructions: List[TACInstruction]) -> str:
    """
    Convenience function to generate pseudocode assembly from TAC.
    
    Args:
        instructions: List of TAC instructions
        
    Returns:
        Pseudocode assembly as string
    """
    generator = AssemblyGenerator()
    return generator.generate(instructions)


# Testing
if __name__ == '__main__':
    from compiler.lexer import lex
    from compiler.parser import parse
    from compiler.semantic import analyze
    from compiler.ir_generator import generate_ir
    from compiler.optimizer import optimize
    
    test_code = """
    int x;
    int y;
    int sum;
    
    x = 10;
    y = 20;
    sum = x + y;
    
    print(sum);
    """
    
    try:
        print("Generating pseudocode assembly...")
        tokens = lex(test_code)
        ast = parse(tokens)
        analyze(ast)
        ir = generate_ir(ast)
        optimized_ir = optimize(ir)
        assembly = generate_assembly(optimized_ir)
        
        print("\nPseudocode Assembly:")
        print(assembly)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
