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
        Apply all optimization passes - EFFICIENT VERSION
        
        Args:
            instructions: Original TAC instructions
            
        Returns:
            Optimized TAC instructions
        """
        self.instructions = instructions
        
        # Apply optimization passes iteratively until no more changes
        changed = True
        iteration = 0
        max_iterations = 10  # Prevent infinite loops
        
        while changed and iteration < max_iterations:
            old_length = len(self.instructions)
            
            # Apply all optimization passes
            self.instructions = self.constant_folding(self.instructions)
            self.instructions = self.copy_propagation(self.instructions)
            self.instructions = self.algebraic_simplification(self.instructions)
            self.instructions = self.strength_reduction(self.instructions)
            self.instructions = self.dead_code_elimination(self.instructions)
            
            # Check if any changes were made
            changed = len(self.instructions) != old_length
            iteration += 1
        
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
    
    def copy_propagation(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Copy propagation optimization - EFFICIENT VERSION
        
        Eliminates unnecessary copy operations by propagating the original value.
        For example: 
            t1 = x
            t2 = t1
            y = t2
        becomes:
            y = x
        
        Args:
            instructions: Original instructions
            
        Returns:
            Instructions with copy propagation applied
        """
        optimized = []
        copies: Dict[str, str] = {}  # Maps variable -> its source
        
        for instr in instructions:
            if isinstance(instr, TACAssign):
                # Follow the copy chain to find the original source
                src = instr.src
                while src in copies:
                    src = copies[src]
                
                # Check if this is a simple copy (not involving operations)
                if src != instr.dest and self._is_temp(instr.dest):
                    # Record the copy
                    copies[instr.dest] = src
                    # Still emit the instruction but with the final source
                    optimized.append(TACAssign(instr.dest, src))
                else:
                    optimized.append(TACAssign(instr.dest, src))
                    # If destination is not a temp, don't track it
                    if not self._is_temp(instr.dest) and instr.dest in copies:
                        del copies[instr.dest]
            
            elif isinstance(instr, TACBinaryOp):
                # Propagate copies in operands
                left = instr.left
                while left in copies:
                    left = copies[left]
                
                right = instr.right
                while right in copies:
                    right = copies[right]
                
                optimized.append(TACBinaryOp(instr.dest, left, instr.op, right))
                
                # Destination is redefined, remove from copies
                if instr.dest in copies:
                    del copies[instr.dest]
            
            elif isinstance(instr, TACUnaryOp):
                # Propagate copies in operand
                operand = instr.operand
                while operand in copies:
                    operand = copies[operand]
                
                optimized.append(TACUnaryOp(instr.dest, instr.op, operand))
                
                # Destination is redefined, remove from copies
                if instr.dest in copies:
                    del copies[instr.dest]
            
            elif isinstance(instr, TACIfFalse):
                # Propagate copy in condition
                condition = instr.condition
                while condition in copies:
                    condition = copies[condition]
                
                optimized.append(TACIfFalse(condition, instr.label))
            
            elif isinstance(instr, TACPrint):
                # Propagate copy in print value
                value = instr.value
                while value in copies:
                    value = copies[value]
                
                optimized.append(TACPrint(value))
            
            else:
                # Labels, gotos, var declarations - keep as is
                optimized.append(instr)
        
        return optimized
    
    def algebraic_simplification(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Algebraic simplification optimization - EFFICIENT VERSION
        
        Simplifies algebraic expressions using mathematical identities:
        - x + 0 = x
        - x - 0 = x
        - x * 1 = x
        - x * 0 = 0
        - x / 1 = x
        - x || true = true
        - x && false = false
        
        Args:
            instructions: Original instructions
            
        Returns:
            Instructions with algebraic simplification applied
        """
        optimized = []
        
        for instr in instructions:
            if isinstance(instr, TACBinaryOp):
                simplified = False
                
                # Check for identity operations
                if instr.op == '+' and instr.right == '0':
                    # x + 0 = x
                    optimized.append(TACAssign(instr.dest, instr.left))
                    simplified = True
                elif instr.op == '+' and instr.left == '0':
                    # 0 + x = x
                    optimized.append(TACAssign(instr.dest, instr.right))
                    simplified = True
                elif instr.op == '-' and instr.right == '0':
                    # x - 0 = x
                    optimized.append(TACAssign(instr.dest, instr.left))
                    simplified = True
                elif instr.op == '*' and instr.right == '1':
                    # x * 1 = x
                    optimized.append(TACAssign(instr.dest, instr.left))
                    simplified = True
                elif instr.op == '*' and instr.left == '1':
                    # 1 * x = x
                    optimized.append(TACAssign(instr.dest, instr.right))
                    simplified = True
                elif instr.op == '*' and (instr.right == '0' or instr.left == '0'):
                    # x * 0 = 0 or 0 * x = 0
                    optimized.append(TACAssign(instr.dest, '0'))
                    simplified = True
                elif instr.op == '/' and instr.right == '1':
                    # x / 1 = x
                    optimized.append(TACAssign(instr.dest, instr.left))
                    simplified = True
                elif instr.op == '||' and (instr.left == 'true' or instr.right == 'true'):
                    # x || true = true or true || x = true
                    optimized.append(TACAssign(instr.dest, 'true'))
                    simplified = True
                elif instr.op == '||' and instr.left == 'false':
                    # false || x = x
                    optimized.append(TACAssign(instr.dest, instr.right))
                    simplified = True
                elif instr.op == '||' and instr.right == 'false':
                    # x || false = x
                    optimized.append(TACAssign(instr.dest, instr.left))
                    simplified = True
                elif instr.op == '&&' and (instr.left == 'false' or instr.right == 'false'):
                    # x && false = false or false && x = false
                    optimized.append(TACAssign(instr.dest, 'false'))
                    simplified = True
                elif instr.op == '&&' and instr.left == 'true':
                    # true && x = x
                    optimized.append(TACAssign(instr.dest, instr.right))
                    simplified = True
                elif instr.op == '&&' and instr.right == 'true':
                    # x && true = x
                    optimized.append(TACAssign(instr.dest, instr.left))
                    simplified = True
                
                if not simplified:
                    optimized.append(instr)
            else:
                optimized.append(instr)
        
        return optimized
    
    def strength_reduction(self, instructions: List[TACInstruction]) -> List[TACInstruction]:
        """
        Strength reduction optimization - EFFICIENT VERSION
        
        Replaces expensive operations with cheaper equivalent ones:
        - x * 2 -> x + x
        - x * 4 -> x << 2 (represented as addition chain)
        - x / 2 -> x >> 1 (represented as division, but noted)
        
        Args:
            instructions: Original instructions
            
        Returns:
            Instructions with strength reduction applied
        """
        optimized = []
        
        for instr in instructions:
            if isinstance(instr, TACBinaryOp):
                reduced = False
                
                # Multiply by 2: x * 2 = x + x
                if instr.op == '*' and instr.right == '2':
                    optimized.append(TACBinaryOp(instr.dest, instr.left, '+', instr.left))
                    reduced = True
                elif instr.op == '*' and instr.left == '2':
                    optimized.append(TACBinaryOp(instr.dest, instr.right, '+', instr.right))
                    reduced = True
                
                if not reduced:
                    optimized.append(instr)
            else:
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
        EFFICIENT VERSION - More aggressive elimination
        
        Args:
            instructions: TAC instructions
            
        Returns:
            Instructions with unused temps removed
        """
        # Iteratively remove unused temps until no more can be removed
        changed = True
        current_instructions = instructions
        
        while changed:
            # First pass: find all used variables
            used_vars = set()
            
            for instr in current_instructions:
                if isinstance(instr, TACAssign):
                    if self._is_temp(instr.src) or not self._is_temp(instr.dest):
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
            for instr in current_instructions:
                keep = True
                
                if isinstance(instr, (TACAssign, TACBinaryOp, TACUnaryOp)):
                    dest = instr.dest
                    if self._is_temp(dest) and dest not in used_vars:
                        keep = False
                
                if keep:
                    optimized.append(instr)
            
            # Check if any changes were made
            changed = len(optimized) != len(current_instructions)
            current_instructions = optimized
        
        return current_instructions
    
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
