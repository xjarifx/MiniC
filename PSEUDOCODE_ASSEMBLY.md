# Phase 6 Pseudocode Assembly - Implementation Notes

## Overview

Phase 6 has been converted from generating real x86-64 assembly to generating **readable pseudocode assembly** for educational purposes.

## Changes Made

### 1. Assembly Generator (`compiler/asmgen.py`)

- Completely rewritten to generate human-readable pseudocode
- Removed all x86-64 specific instructions (movq, pushq, cmpq, etc.)
- Replaced with simple, clear operations

### 2. Pseudocode Assembly Format

**Structure:**

```
======================================================================
PSEUDOCODE ASSEMBLY
======================================================================

PROGRAM START:

  // Allocate memory for variables
  DECLARE variable_name
  ...

  [instructions]

  RETURN 0

PROGRAM END
======================================================================
```

**Instructions:**

- `SET dest = value` - Assignment
- `SET dest = ADD(left, right)` - Binary operations
- `SET dest = NEGATE(operand)` - Unary operations
- `PRINT(value)` - Output
- `IF condition == false THEN GOTO label` - Conditional branch
- `GOTO label` - Unconditional jump
- `label:` - Label definition
- `RETURN 0` - Program end

**Operations:**

- Arithmetic: `ADD`, `SUBTRACT`, `MULTIPLY`, `DIVIDE`, `MODULO`
- Comparison: `LESS_THAN`, `GREATER_THAN`, `LESS_EQUAL`, `GREATER_EQUAL`, `EQUALS`, `NOT_EQUALS`
- Logical: `AND`, `OR`, `NOT`, `NEGATE`

### 3. File Extensions

- Changed from `.s` (assembly source) to `.asm` (assembly-like pseudocode)
- Updated all references in `minic.py`

### 4. User Messages

- Updated to clarify this is pseudocode, not executable assembly
- Removed gcc compilation instructions
- Added educational purpose note

## Examples

### Simple Assignment

**MiniC Code:**

```c
int x;
x = 42;
print(x);
```

**Pseudocode Assembly:**

```
DECLARE x

SET x = 42
PRINT(x)
```

### Binary Operations

**MiniC Code:**

```c
int a;
int b;
int sum;

a = 15;
b = 4;
sum = a + b;
print(sum);
```

**Pseudocode Assembly:**

```
DECLARE a
DECLARE b
DECLARE sum
DECLARE t0

SET a = 15
SET b = 4
SET t0 = ADD(a, b)
SET sum = t0
PRINT(sum)
```

### Control Flow (If-Else)

**MiniC Code:**

```c
int x;
int y;
int max;

x = 42;
y = 17;

if (x > y) {
    max = x;
} else {
    max = y;
}
print(max);
```

**Pseudocode Assembly:**

```
DECLARE x
DECLARE y
DECLARE max
DECLARE t0

SET x = 42
SET y = 17
SET t0 = GREATER_THAN(x, y)
IF t0 == false THEN GOTO L0
SET max = x
GOTO L1

L0:
SET max = y

L1:
PRINT(max)
```

### Loops

**MiniC Code:**

```c
int counter;
counter = 1;

while (counter <= 5) {
    print(counter);
    counter = counter + 1;
}
```

**Pseudocode Assembly:**

```
DECLARE counter
DECLARE t0
DECLARE t1

SET counter = 1

L0:
SET t0 = LESS_EQUAL(counter, 5)
IF t0 == false THEN GOTO L1
PRINT(counter)
SET t1 = ADD(counter, 1)
SET counter = t1
GOTO L0

L1:
```

## Benefits of Pseudocode Assembly

1. **Educational Value**: Students can understand the flow without learning x86-64
2. **Readability**: Operations are self-documenting (ADD vs addq)
3. **Platform Independence**: Not tied to any specific architecture
4. **Focus on Concepts**: Emphasizes compiler concepts over machine details
5. **Debugging**: Much easier to trace through and understand

## Comparison: Before vs After

### Before (x86-64):

```assembly
    movq    $10, %rax
    movq    %rax, -8(%rbp)
    movq    $5, %rax
    movq    %rax, -16(%rbp)
    movq    -8(%rbp), %rax
    movq    -16(%rbp), %rbx
    addq    %rbx, %rax
    movq    %rax, -24(%rbp)
```

### After (Pseudocode):

```
SET x = 10
SET y = 5
SET t0 = ADD(x, y)
SET sum = t0
```

## Usage

```bash
# Generate pseudocode assembly
python minic.py program.mc

# View the pseudocode assembly
python minic.py program.mc --show-asm

# Output to specific file
python minic.py program.mc -o myprogram.asm
```

## Files Modified

1. `compiler/asmgen.py` - Complete rewrite for pseudocode generation
2. `minic.py` - Updated file extensions and user messages
3. `examples/optimization_demo.mc` - New example to show optimization effects

## Notes

- The pseudocode is **not executable** - it's for educational purposes
- All optimizations from Phase 5 still work and are visible in the output
- Labels (L0, L1, etc.) show control flow structure
- Temporary variables (t0, t1, etc.) show intermediate computations
- To generate actual executable code, a real backend would be needed

## Future Enhancements

Could add:

- Color-coded output for different instruction types
- Comments showing original MiniC source lines
- Basic block annotations
- Control flow graph visualization
- Stack frame diagrams
