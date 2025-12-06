"""
MiniC Assembly Generator
Generates x86-64 assembly code directly from IR (bypassing C compiler).
"""

from typing import List, Dict
from compiler.ir_generator import *


class AssemblyGenerator:
    """
    Generates x86-64 assembly code from Three-Address Code.
    This assembly can be assembled directly to machine code using 'as' and 'ld'.
    """
    
    def __init__(self):
        self.asm_lines: List[str] = []
        self.var_offsets: Dict[str, int] = {}  # Variable name -> stack offset
        self.current_offset = 0
        self.string_literals: List[str] = []
        self.label_count = 0
    
    def generate(self, instructions: List[TACInstruction]) -> str:
        """
        Generate x86-64 assembly code from TAC instructions.
        
        Args:
            instructions: List of TAC instructions
            
        Returns:
            x86-64 assembly code as string
        """
        self.asm_lines = []
        self.var_offsets = {}
        self.current_offset = 0
        
        # Header
        self.asm_lines.append("    .section .data")
        self.asm_lines.append("fmt_int:")
        self.asm_lines.append('    .string "%d\\n"')
        self.asm_lines.append("")
        
        # Text section
        self.asm_lines.append("    .section .text")
        self.asm_lines.append("    .globl main")
        self.asm_lines.append("")
        self.asm_lines.append("main:")
        self.asm_lines.append("    # Function prologue")
        self.asm_lines.append("    pushq   %rbp")
        self.asm_lines.append("    movq    %rsp, %rbp")
        
        # Allocate space for variables
        self._allocate_variables(instructions)
        
        # Generate code for each instruction
        for instr in instructions:
            self._generate_instruction(instr)
        
        # Function epilogue
        self.asm_lines.append("")
        self.asm_lines.append("    # Function epilogue")
        self.asm_lines.append("    movq    $0, %rax")
        self.asm_lines.append("    movq    %rbp, %rsp")
        self.asm_lines.append("    popq    %rbp")
        self.asm_lines.append("    ret")
        
        # Add GNU stack note to prevent executable stack warning
        self.asm_lines.append("")
        self.asm_lines.append("    .section .note.GNU-stack,\"\",%progbits")
        
        return "\n".join(self.asm_lines) + "\n"
    
    def _allocate_variables(self, instructions: List[TACInstruction]):
        """Allocate stack space for all variables"""
        variables = set()
        
        # Collect all variables
        for instr in instructions:
            if isinstance(instr, TACVarDecl):
                variables.add(instr.name)
            elif isinstance(instr, TACAssign):
                if not self._is_constant(instr.dest):
                    variables.add(instr.dest)
            elif isinstance(instr, TACBinaryOp):
                variables.add(instr.dest)
            elif isinstance(instr, TACUnaryOp):
                variables.add(instr.dest)
        
        # Allocate stack space
        if variables:
            total_size = len(variables) * 8  # 8 bytes per variable
            self.asm_lines.append(f"    subq    ${total_size}, %rsp")
            self.asm_lines.append("")
            
            # Map variables to stack offsets
            offset = -8
            for var in sorted(variables):
                self.var_offsets[var] = offset
                offset -= 8
    
    def _generate_instruction(self, instr: TACInstruction):
        """Generate assembly for a single TAC instruction"""
        if isinstance(instr, TACVarDecl):
            # Variable declarations are handled in allocation
            self.asm_lines.append(f"    # var {instr.var_type} {instr.name}")
        
        elif isinstance(instr, TACAssign):
            # dest = src
            self.asm_lines.append(f"    # {instr.dest} = {instr.src}")
            
            if self._is_constant(instr.src):
                # Load constant
                value = instr.src if instr.src not in ['true', 'false'] else ('1' if instr.src == 'true' else '0')
                self.asm_lines.append(f"    movq    ${value}, %rax")
            else:
                # Load from memory
                offset = self.var_offsets.get(instr.src, 0)
                self.asm_lines.append(f"    movq    {offset}(%rbp), %rax")
            
            # Store to destination
            offset = self.var_offsets.get(instr.dest, 0)
            self.asm_lines.append(f"    movq    %rax, {offset}(%rbp)")
        
        elif isinstance(instr, TACBinaryOp):
            # dest = left op right
            self.asm_lines.append(f"    # {instr.dest} = {instr.left} {instr.op} {instr.right}")
            
            # Load left operand into %rax
            if self._is_constant(instr.left):
                value = instr.left if instr.left not in ['true', 'false'] else ('1' if instr.left == 'true' else '0')
                self.asm_lines.append(f"    movq    ${value}, %rax")
            else:
                offset = self.var_offsets.get(instr.left, 0)
                self.asm_lines.append(f"    movq    {offset}(%rbp), %rax")
            
            # Load right operand into %rbx
            if self._is_constant(instr.right):
                value = instr.right if instr.right not in ['true', 'false'] else ('1' if instr.right == 'true' else '0')
                self.asm_lines.append(f"    movq    ${value}, %rbx")
            else:
                offset = self.var_offsets.get(instr.right, 0)
                self.asm_lines.append(f"    movq    {offset}(%rbp), %rbx")
            
            # Perform operation
            if instr.op == '+':
                self.asm_lines.append("    addq    %rbx, %rax")
            elif instr.op == '-':
                self.asm_lines.append("    subq    %rbx, %rax")
            elif instr.op == '*':
                self.asm_lines.append("    imulq   %rbx, %rax")
            elif instr.op == '/':
                self.asm_lines.append("    cqo")  # Sign extend
                self.asm_lines.append("    idivq   %rbx")
            elif instr.op == '%':
                self.asm_lines.append("    cqo")
                self.asm_lines.append("    idivq   %rbx")
                self.asm_lines.append("    movq    %rdx, %rax")  # Remainder in rdx
            elif instr.op in ['<', '>', '<=', '>=', '==', '!=']:
                # Comparison operations
                self.asm_lines.append("    cmpq    %rbx, %rax")
                
                op_map = {
                    '<': 'setl',
                    '>': 'setg',
                    '<=': 'setle',
                    '>=': 'setge',
                    '==': 'sete',
                    '!=': 'setne'
                }
                self.asm_lines.append(f"    {op_map[instr.op]}  %al")
                self.asm_lines.append("    movzbq  %al, %rax")
            elif instr.op == '&&':
                self.asm_lines.append("    andq    %rbx, %rax")
            elif instr.op == '||':
                self.asm_lines.append("    orq     %rbx, %rax")
            
            # Store result
            offset = self.var_offsets.get(instr.dest, 0)
            self.asm_lines.append(f"    movq    %rax, {offset}(%rbp)")
        
        elif isinstance(instr, TACUnaryOp):
            # dest = op operand
            self.asm_lines.append(f"    # {instr.dest} = {instr.op}{instr.operand}")
            
            if self._is_constant(instr.operand):
                value = instr.operand
                self.asm_lines.append(f"    movq    ${value}, %rax")
            else:
                offset = self.var_offsets.get(instr.operand, 0)
                self.asm_lines.append(f"    movq    {offset}(%rbp), %rax")
            
            if instr.op == '-':
                self.asm_lines.append("    negq    %rax")
            elif instr.op == '!':
                self.asm_lines.append("    xorq    $1, %rax")
            
            offset = self.var_offsets.get(instr.dest, 0)
            self.asm_lines.append(f"    movq    %rax, {offset}(%rbp)")
        
        elif isinstance(instr, TACLabel):
            # Label
            self.asm_lines.append(f"{instr.label}:")
        
        elif isinstance(instr, TACGoto):
            # Unconditional jump
            self.asm_lines.append(f"    jmp     {instr.label}")
        
        elif isinstance(instr, TACIfFalse):
            # Conditional jump
            self.asm_lines.append(f"    # if !{instr.condition} goto {instr.label}")
            
            if self._is_constant(instr.condition):
                value = '1' if instr.condition == 'true' else '0'
                self.asm_lines.append(f"    movq    ${value}, %rax")
            else:
                offset = self.var_offsets.get(instr.condition, 0)
                self.asm_lines.append(f"    movq    {offset}(%rbp), %rax")
            
            self.asm_lines.append("    cmpq    $0, %rax")
            self.asm_lines.append(f"    je      {instr.label}")
        
        elif isinstance(instr, TACPrint):
            # Print statement
            self.asm_lines.append(f"    # print {instr.value}")
            
            if self._is_constant(instr.value):
                value = instr.value if instr.value not in ['true', 'false'] else ('1' if instr.value == 'true' else '0')
                self.asm_lines.append(f"    movq    ${value}, %rsi")
            else:
                offset = self.var_offsets.get(instr.value, 0)
                self.asm_lines.append(f"    movq    {offset}(%rbp), %rsi")
            
            self.asm_lines.append("    leaq    fmt_int(%rip), %rdi")
            self.asm_lines.append("    movq    $0, %rax")
            self.asm_lines.append("    call    printf@PLT")
        
        self.asm_lines.append("")
    
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
    Convenience function to generate assembly from TAC.
    
    Args:
        instructions: List of TAC instructions
        
    Returns:
        x86-64 assembly code as string
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
        print("Generating assembly...")
        tokens = lex(test_code)
        ast = parse(tokens)
        analyze(ast)
        ir = generate_ir(ast)
        optimized_ir = optimize(ir)
        assembly = generate_assembly(optimized_ir)
        
        print("\nx86-64 Assembly Code:")
        print("=" * 70)
        print(assembly)
        print("=" * 70)
        
        # Save to file
        with open("/tmp/output.s", "w") as f:
            f.write(assembly)
        print("\nSaved to /tmp/output.s")
        print("\nTo assemble and run:")
        print("  gcc /tmp/output.s -o /tmp/program -no-pie")
        print("  /tmp/program")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
