"""
MiniC Optimizer
Performs optimization passes on Three-Address Code.
"""

from typing import List, Set, Dict, Optional
from compiler.ir_generator import *


class Optimizer:
    """
    Optimizer for TAC intermediate representation.
    
    Optimizations implemented:
    1. Constant folding - Evaluate constant expressions at compile time
    2. Dead code elimination - Remove unreachable code and unused temporaries
    """
    
    def __init__(self):
        self.instructions: List[TACInstruction] = []
    
    def optimize(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Apply all optimization passes.
        
        Args:
            instructions: Original TAC instructions
            
        Returns:
            Optimized TAC instructions
        """
        self.instructions = instructions
        
        # Apply optimization passes
        self.instructions = self.constant_folding(self.instructions)
        self.instructions = self.dead_code_elimination(self.instructions)
        
        return self.instructions
    
    def constant_folding(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Constant folding optimization.
        
        Evaluates constant expressions at compile time.
        For example: t0 = 2 + 3 becomes t0 = 5
        
        Args:
            instructions: Original instructions
            
        Returns:
            Instructions with constant folding applied
        """
        optimized = []
        constants: Dict[str, any] = {}  # Track constant values
        
        for instr in instructions:
            if isinstance(instr, TACAssign):
                # Check if source is a constant
                if self._is_constant(instr.src):
                    value = self._get_constant_value(instr.src)
                    # Only track temporaries as constants, not user variables
                    if self._is_temp(instr.dest):
                        constants[instr.dest] = value
                    optimized.append(instr)
                elif instr.src in constants:
                    # Propagate constant
                    optimized.append(TACAssign(instr.dest, self._value_to_string(constants[instr.src])))
                    if self._is_temp(instr.dest):
                        constants[instr.dest] = constants[instr.src]
                else:
                    optimized.append(instr)
                    if instr.dest in constants:
                        del constants[instr.dest]
            
            elif isinstance(instr, TACBinaryOp):
                # Try to fold binary operation
                left_const = self._is_constant(instr.left) or instr.left in constants
                right_const = self._is_constant(instr.right) or instr.right in constants
                
                if left_const and right_const:
                    # Both operands are constants - fold the operation
                    try:
                        if instr.left in constants:
                            left_val = constants[instr.left]
                        else:
                            left_val = self._get_constant_value(instr.left)
                        
                        if instr.right in constants:
                            right_val = constants[instr.right]
                        else:
                            right_val = self._get_constant_value(instr.right)
                        
                        result = self._evaluate_binary_op(instr.op, left_val, right_val)
                        
                        if result is not None:
                            # Replace with assignment of constant result
                            optimized.append(TACAssign(instr.dest, self._value_to_string(result)))
                            if self._is_temp(instr.dest):
                                constants[instr.dest] = result
                        else:
                            # Can't fold (e.g., division by zero, boolean ops)
                            optimized.append(instr)
                            if instr.dest in constants:
                                del constants[instr.dest]
                    except (ValueError, TypeError):
                        # Not actually constants
                        optimized.append(instr)
                        if instr.dest in constants:
                            del constants[instr.dest]
                else:
                    optimized.append(instr)
                    if instr.dest in constants:
                        del constants[instr.dest]
            
            elif isinstance(instr, TACUnaryOp):
                # Try to fold unary operation
                operand_const = self._is_constant(instr.operand) or instr.operand in constants
                
                if operand_const:
                    # Operand is constant - fold the operation
                    try:
                        if instr.operand in constants:
                            operand_val = constants[instr.operand]
                        else:
                            operand_val = self._get_constant_value(instr.operand)
                        
                        result = self._evaluate_unary_op(instr.op, operand_val)
                        
                        if result is not None:
                            # Replace with assignment of constant result
                            optimized.append(TACAssign(instr.dest, self._value_to_string(result)))
                            if self._is_temp(instr.dest):
                                constants[instr.dest] = result
                        else:
                            optimized.append(instr)
                            if instr.dest in constants:
                                del constants[instr.dest]
                    except (ValueError, TypeError):
                        # Not actually constant
                        optimized.append(instr)
                        if instr.dest in constants:
                            del constants[instr.dest]
                else:
                    optimized.append(instr)
                    if instr.dest in constants:
                        del constants[instr.dest]
            
            else:
                # Other instructions - keep as is
                optimized.append(instr)
        
        return optimized
    
    def dead_code_elimination(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Dead code elimination optimization.
        
        Removes:
        1. Unreachable code after unconditional jumps
        2. Unused temporary variables
        
        Args:
            instructions: Original instructions
            
        Returns:
            Instructions with dead code removed
        """
        # First pass: identify reachable code
        reachable = self._find_reachable_code(instructions)
        
        # Second pass: remove unreachable instructions
        optimized = []
        for i, instr in enumerate(instructions):
            if i in reachable:
                optimized.append(instr)
        
        # Third pass: remove unused temporaries
        optimized = self._remove_unused_temps(optimized)
        
        return optimized
    
    def _find_reachable_code(self, instructions: List[TACInstruction]) -> Set[int]:
        """
        Find all reachable instruction indices using control flow analysis.
        
        Args:
            instructions: TAC instructions
            
        Returns:
            Set of reachable instruction indices
        """
        # Build label -> index mapping
        labels: Dict[str, int] = {}
        for i, instr in enumerate(instructions):
            if isinstance(instr, TACLabel):
                labels[instr.label] = i
        
        # Mark reachable instructions
        reachable = set()
        worklist = [0]  # Start from first instruction
        
        while worklist:
            idx = worklist.pop()
            
            if idx < 0 or idx >= len(instructions) or idx in reachable:
                continue
            
            reachable.add(idx)
            instr = instructions[idx]
            
            # Determine next instructions based on control flow
            if isinstance(instr, TACGoto):
                # Unconditional jump
                if instr.label in labels:
                    worklist.append(labels[instr.label])
            elif isinstance(instr, TACIfFalse):
                # Conditional jump - both paths are reachable
                if instr.label in labels:
                    worklist.append(labels[instr.label])
                if idx + 1 < len(instructions):
                    worklist.append(idx + 1)
            else:
                # Sequential execution
                if idx + 1 < len(instructions):
                    worklist.append(idx + 1)
        
        return reachable
    
    def _remove_unused_temps(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Remove assignments to temporary variables that are never used.
        
        Args:
            instructions: TAC instructions
            
        Returns:
            Instructions with unused temps removed
        """
        # First pass: find all used variables
        used_vars = set()
        
        for instr in instructions:
            if isinstance(instr, TACAssign):
                if self._is_temp(instr.src):
                    used_vars.add(instr.src)
            elif isinstance(instr, TACBinaryOp):
                if self._is_temp(instr.left):
                    used_vars.add(instr.left)
                if self._is_temp(instr.right):
                    used_vars.add(instr.right)
            elif isinstance(instr, TACUnaryOp):
                if self._is_temp(instr.operand):
                    used_vars.add(instr.operand)
            elif isinstance(instr, TACIfFalse):
                if self._is_temp(instr.condition):
                    used_vars.add(instr.condition)
            elif isinstance(instr, TACPrint):
                if self._is_temp(instr.value):
                    used_vars.add(instr.value)
        
        # Second pass: remove assignments to unused temps
        optimized = []
        for instr in instructions:
            keep = True
            
            if isinstance(instr, (TACAssign, TACBinaryOp, TACUnaryOp)):
                dest = instr.dest
                if self._is_temp(dest) and dest not in used_vars:
                    keep = False
            
            if keep:
                optimized.append(instr)
        
        return optimized
    
    # ========================================================================
    # Helper methods
    # ========================================================================
    
    def _is_constant(self, value: str) -> bool:
        """Check if value is a constant literal"""
        if value in ['true', 'false']:
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False
    
    def _get_constant_value(self, value: str):
        """Get the actual value of a constant"""
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            return int(value)
    
    def _is_temp(self, name: str) -> bool:
        """Check if a variable name is a temporary (starts with 't' followed by digits)"""
        return name.startswith('t') and name[1:].isdigit()
    
    def _value_to_string(self, value) -> str:
        """Convert a constant value to its string representation"""
        if isinstance(value, bool):
            return 'true' if value else 'false'
        else:
            return str(value)
    
    def _evaluate_binary_op(self, op: str, left, right):
        """Evaluate a binary operation on constants"""
        try:
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    return None  # Don't fold division by zero
                return left // right  # Integer division
            elif op == '%':
                if right == 0:
                    return None
                return left % right
            elif op == '<':
                return left < right
            elif op == '>':
                return left > right
            elif op == '<=':
                return left <= right
            elif op == '>=':
                return left >= right
            elif op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '&&':
                return left and right
            elif op == '||':
                return left or right
            else:
                return None
        except:
            return None
    
    def _evaluate_unary_op(self, op: str, operand):
        """Evaluate a unary operation on a constant"""
        try:
            if op == '-':
                return -operand
            elif op == '!':
                return not operand
            else:
                return None
        except:
            return None


def optimize(instructions: List[TACInstruction]) -> List[TACInstruction]:
    """
    Convenience function to optimize TAC instructions.
    
    Args:
        instructions: Original TAC instructions
        
    Returns:
        Optimized TAC instructions
    """
    optimizer = Optimizer()
    return optimizer.optimize(instructions)


# Testing
if __name__ == '__main__':
    from compiler.lexer import lex
    from compiler.parser import parse
    from compiler.semantic import analyze
    from compiler.ir_generator import generate_ir, print_ir
    
    # Test constant folding
    test_code = """
    int x;
    int y;
    int z;
    
    x = 2 + 3;
    y = x * 4;
    z = 10 - 5;
    
    print(z);
    
    if (5 > 3) {
        print(100);
    }
    """
    
    try:
        print("Original IR:")
        print("=" * 50)
        tokens = lex(test_code)
        ast = parse(tokens)
        analyze(ast)
        ir = generate_ir(ast)
        print(print_ir(ir))
        
        print("\n\nOptimized IR:")
        print("=" * 50)
        optimized_ir = optimize(ir)
        print(print_ir(optimized_ir))
        
        print(f"\n\nOriginal instructions: {len(ir)}")
        print(f"Optimized instructions: {len(optimized_ir)}")
        print(f"Reduction: {len(ir) - len(optimized_ir)} instructions")
        
    except Exception as e:
        print(f"Error: {e}")
