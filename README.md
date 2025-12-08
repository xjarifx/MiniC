# MiniC Compiler

A comprehensive educational compiler for the MiniC language, featuring a six-phase compilation pipeline with intermediate representation, aggressive optimization, and readable pseudocode assembly output.

## Table of Contents

- [Quick Start](#quick-start)
- [Language Reference](#language-reference)
  - [Introduction](#introduction)
  - [Basic Syntax](#basic-syntax)
  - [Data Types](#data-types)
  - [Variables](#variables)
  - [Operators](#operators)
  - [Control Flow](#control-flow)
  - [Input/Output](#inputoutput)
  - [Comments](#comments)
  - [Complete Examples](#complete-examples)
  - [Language Limitations](#language-limitations)
  - [Quick Reference Card](#quick-reference-card)
- [Compiler Phases](#compiler-phases)
- [Pseudocode Assembly](#pseudocode-assembly)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Command-Line Options](#command-line-options)
- [Example Programs](#example-programs)
- [Web Interface](#web-interface)
- [Technical Details](#technical-details)

---

## Quick Start

```bash
# Clone or download this repository
cd MiniC

# Run the compiler on an example program
python minic.py examples/hello.mc

# View all compiler phases
python minic.py examples/hello.mc --show-all

# Use the web interface
python web_interface.py
# Then open http://localhost:5000
```

---

## Language Reference

### Introduction

**MiniC** is a minimalist C-like programming language designed for educational purposes. It provides core programming concepts without the complexity of a full-featured language.

**What MiniC has:**

- Two data types: `int` and `bool`
- Variables and assignments
- Arithmetic, comparison, and logical operators
- Conditional statements (`if-else`)
- Loops (`while`)
- Output (`print`)
- Comments

**What MiniC doesn't have:**

- Functions
- Arrays
- Strings
- User input
- Pointers
- Floating-point numbers

This simplicity makes it perfect for learning compiler design!

---

### Basic Syntax

#### Program Structure

A MiniC program is a sequence of statements. All code must be at the top level (no functions).

**Hello World:**

```c
{
    int x;
    x = 42;
    print(x);
}
```

#### Statements

Every statement ends with a semicolon `;`:

```c
int age;               // Variable declaration
age = 25;              // Assignment
print(age);            // Print statement
```

#### Blocks

Code blocks are enclosed in curly braces `{ }`:

```c
if (x > 5) {
    print(x);
    x = x - 1;
}
```

---

### Data Types

MiniC supports two data types:

#### Integer (`int`)

Whole numbers (positive, negative, or zero):

```c
int count;
count = 42;

int temperature;
temperature = -15;

int zero;
zero = 0;
```

**Range**: Standard 32-bit signed integers (-2,147,483,648 to 2,147,483,647)

#### Boolean (`bool`)

Logical values (`true` or `false`):

```c
bool isReady;
isReady = true;

bool hasError;
hasError = false;

bool flag;
flag = false;
```

**Note**: In output, `true` displays as `1` and `false` displays as `0`.

---

### Variables

#### Declaration

Variables must be declared before use:

```c
int age;           // Declare integer
bool isActive;     // Declare boolean
```

#### Assignment

After declaration, you can assign values:

```c
int count;
count = 10;        // Assign 10 to count

bool ready;
ready = true;      // Assign true to ready
```

#### Multiple Variables

```c
int x;
int y;
int z;

x = 5;
y = 10;
z = x + y;         // z becomes 15
```

#### Variable Names (Identifiers)

**Valid names:**

- Must start with a letter (a-z, A-Z)
- Can contain letters, digits (0-9), and underscores (\_)
- Cannot be a reserved keyword

```c
int age;           // ✓ Valid
int user_count;    // ✓ Valid
int value123;      // ✓ Valid
int _temp;         // ✓ Valid

int 3count;        // ✗ Invalid (starts with digit)
int my-var;        // ✗ Invalid (contains hyphen)
int while;         // ✗ Invalid (reserved keyword)
```

**Reserved Keywords:**

```
int, bool, true, false, if, else, while, print
```

---

### Operators

#### Arithmetic Operators

For `int` types only:

| Operator | Operation      | Example  | Result |
| -------- | -------------- | -------- | ------ |
| `+`      | Addition       | `5 + 3`  | `8`    |
| `-`      | Subtraction    | `5 - 3`  | `2`    |
| `*`      | Multiplication | `5 * 3`  | `15`   |
| `/`      | Division       | `10 / 3` | `3`    |
| `%`      | Modulo         | `10 % 3` | `1`    |

```c
{
    int a;
    int b;
    int result;

    a = 10;
    b = 3;

    result = a + b;    // 13
    print(result);

    result = a * b;    // 30
    print(result);

    result = a / b;    // 3 (integer division)
    print(result);

    result = a % b;    // 1 (remainder)
    print(result);
}
```

**Important**: Division is integer division (truncates decimal part).

#### Comparison Operators

Compare values and return `bool`:

| Operator | Comparison       | Example  | Result  |
| -------- | ---------------- | -------- | ------- |
| `<`      | Less than        | `5 < 10` | `true`  |
| `>`      | Greater than     | `5 > 10` | `false` |
| `<=`     | Less or equal    | `5 <= 5` | `true`  |
| `>=`     | Greater or equal | `5 >= 3` | `true`  |
| `==`     | Equal to         | `5 == 5` | `true`  |
| `!=`     | Not equal to     | `5 != 3` | `true`  |

```c
{
    int x;
    bool result;

    x = 10;

    result = x > 5;     // true
    print(result);      // Prints: 1

    result = x == 10;   // true
    print(result);      // Prints: 1

    result = x < 5;     // false
    print(result);      // Prints: 0
}
```

#### Logical Operators

For `bool` types:

| Operator | Operation | Example           | Result  |
| -------- | --------- | ----------------- | ------- |
| `&&`     | AND       | `true && false`   | `false` |
| `\|\|`   | OR        | `true \|\| false` | `true`  |
| `!`      | NOT       | `!true`           | `false` |

```c
{
    bool a;
    bool b;
    bool result;

    a = true;
    b = false;

    result = a && b;    // false (both must be true)
    print(result);      // Prints: 0

    result = a || b;    // true (at least one is true)
    print(result);      // Prints: 1

    result = !a;        // false (opposite of true)
    print(result);      // Prints: 0
}
```

#### Operator Precedence

From highest to lowest:

1. `!` (NOT)
2. `*`, `/`, `%` (Multiplication, Division, Modulo)
3. `+`, `-` (Addition, Subtraction)
4. `<`, `>`, `<=`, `>=` (Comparison)
5. `==`, `!=` (Equality)
6. `&&` (AND)
7. `||` (OR)

Use parentheses `()` to override precedence:

```c
int result;
result = 2 + 3 * 4;      // 14 (multiply first)
result = (2 + 3) * 4;    // 20 (add first)
```

---

### Control Flow

#### If-Else Statements

Execute code conditionally:

**Syntax:**

```c
if (condition) {
    // Code when condition is true
} else {
    // Code when condition is false
}
```

**Examples:**

```c
{
    int x;
    x = 10;

    if (x > 5) {
        print(1);    // Prints: 1 (condition is true)
    } else {
        print(0);
    }
}
```

```c
{
    int age;
    age = 15;

    if (age >= 18) {
        print(1);    // Adult
    } else {
        print(0);    // Minor (this executes)
    }
}
```

**If without Else:**

```c
{
    int x;
    x = 7;

    if (x > 5) {
        print(x);    // Prints: 7
    }
    // No else branch needed
}
```

**Nested If:**

```c
{
    int x;
    x = 15;

    if (x > 10) {
        if (x < 20) {
            print(1);    // x is between 10 and 20
        }
    }
}
```

#### While Loops

Repeat code while a condition is true:

**Syntax:**

```c
while (condition) {
    // Code to repeat
}
```

**Examples:**

```c
// Countdown from 5 to 1
{
    int count;
    count = 5;

    while (count > 0) {
        print(count);
        count = count - 1;
    }
}
// Output: 5 4 3 2 1
```

```c
// Sum of numbers 1 to 10
{
    int i;
    int sum;

    i = 1;
    sum = 0;

    while (i <= 10) {
        sum = sum + i;
        i = i + 1;
    }

    print(sum);    // Prints: 55
}
```

**Infinite Loop** (careful!):

```c
{
    while (true) {
        print(1);    // This will run forever!
    }
}
```

---

### Input/Output

#### Print Statement

The only I/O operation in MiniC is `print()`:

**Syntax:**

```c
print(expression);
```

**What you can print:**

- Integer values
- Boolean values (as 0 or 1)
- Results of expressions

**Examples:**

```c
{
    int x;
    x = 42;

    print(x);          // Prints: 42
    print(100);        // Prints: 100
    print(x + 10);     // Prints: 52
    print(x * 2);      // Prints: 84
}
```

```c
{
    bool flag;
    flag = true;

    print(flag);       // Prints: 1 (true)

    flag = false;
    print(flag);       // Prints: 0 (false)
}
```

**Note**: Each `print()` outputs a number followed by a newline.

---

### Comments

Comments are ignored by the compiler and help document your code.

#### Single-Line Comments

Use `//` for single-line comments:

```c
{
    // This is a comment
    int x;        // Comments can be at end of line
    x = 42;       // Assign 42 to x
    print(x);
}
```

#### Multi-Line Comments

Use `/* */` for multi-line comments:

```c
{
    /*
     * This is a multi-line comment.
     * It can span multiple lines.
     * Useful for longer explanations.
     */
    int x;
    x = 10;

    /* You can also use it inline */ print(x);
}
```

---

### Complete Examples

#### Example 1: Simple Calculator

```c
{
    int a;
    int b;
    int sum;
    int product;

    a = 15;
    b = 7;

    sum = a + b;
    product = a * b;

    print(sum);        // Prints: 22
    print(product);    // Prints: 105
}
```

#### Example 2: Even or Odd

```c
{
    int num;
    int remainder;

    num = 17;
    remainder = num % 2;

    if (remainder == 0) {
        print(0);      // Even
    } else {
        print(1);      // Odd (prints this)
    }
}
```

#### Example 3: Factorial

```c
{
    int n;
    int factorial;
    int i;

    n = 5;
    factorial = 1;
    i = 1;

    while (i <= n) {
        factorial = factorial * i;
        i = i + 1;
    }

    print(factorial);  // Prints: 120 (5! = 5*4*3*2*1)
}
```

#### Example 4: Fibonacci Sequence

```c
{
    int n;
    int a;
    int b;
    int temp;
    int count;

    n = 10;          // Number of terms
    a = 0;
    b = 1;
    count = 0;

    while (count < n) {
        print(a);
        temp = a + b;
        a = b;
        b = temp;
        count = count + 1;
    }
}
// Output: 0 1 1 2 3 5 8 13 21 34
```

#### Example 5: Prime Number Checker

```c
{
    int num;
    int i;
    int isPrime;

    num = 17;
    isPrime = 1;     // Assume prime (true)
    i = 2;

    while (i < num) {
        if (num % i == 0) {
            isPrime = 0;    // Not prime
        }
        i = i + 1;
    }

    print(isPrime);  // Prints: 1 (17 is prime)
}
```

#### Example 6: Maximum of Two Numbers

```c
{
    int a;
    int b;
    int max;

    a = 25;
    b = 42;

    if (a > b) {
        max = a;
    } else {
        max = b;
    }

    print(max);      // Prints: 42
}
```

#### Example 7: Sum of Digits

```c
{
    int num;
    int digit;
    int sum;

    num = 1234;
    sum = 0;

    while (num > 0) {
        digit = num % 10;     // Get last digit
        sum = sum + digit;
        num = num / 10;       // Remove last digit
    }

    print(sum);      // Prints: 10 (1+2+3+4)
}
```

#### Example 8: Power Function

```c
{
    int base;
    int exponent;
    int result;
    int i;

    base = 2;
    exponent = 8;
    result = 1;
    i = 0;

    while (i < exponent) {
        result = result * base;
        i = i + 1;
    }

    print(result);   // Prints: 256 (2^8)
}
```

---

### Language Limitations

Understanding what MiniC **cannot** do:

#### ❌ No Functions

```c
// ✗ This doesn't work
int add(int a, int b) {
    return a + b;
}
```

MiniC doesn't support functions - all code is sequential statements.

#### ❌ No Arrays

```c
// ✗ This doesn't work
int numbers[10];
```

You must use separate variables.

#### ❌ No Strings

```c
// ✗ This doesn't work
print("Hello World");
```

Only integer and boolean values can be printed.

#### ❌ No User Input

```c
// ✗ This doesn't work
int x;
x = read();
```

All values must be hardcoded or calculated.

#### ❌ No Pointers or References

```c
// ✗ This doesn't work
int* ptr;
```

#### ❌ No Floating Point

```c
// ✗ This doesn't work
float x;
x = 3.14;
```

Only integers are supported.

#### ❌ No Break or Continue

```c
// ✗ This doesn't work
while (true) {
    if (x > 10) {
        break;
    }
}
```

Use conditional logic instead.

#### ❌ No For Loops

```c
// ✗ This doesn't work
for (i = 0; i < 10; i = i + 1) {
    print(i);
}
```

Use `while` loops instead:

```c
// ✓ This works
int i;
i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}
```

#### ❌ No Switch Statements

```c
// ✗ This doesn't work
switch (x) {
    case 1: print(1); break;
    case 2: print(2); break;
}
```

Use if-else chains instead:

```c
// ✓ This works
if (x == 1) {
    print(1);
} else {
    if (x == 2) {
        print(2);
    }
}
```

---

### Quick Reference Card

#### Keywords

```
int, bool, true, false, if, else, while, print
```

#### Data Types

```c
int x;      // Integer
bool flag;  // Boolean
```

#### Operators

```c
+  -  *  /  %              // Arithmetic
<  >  <=  >=  ==  !=       // Comparison
&&  ||  !                   // Logical
```

#### Control Flow

```c
if (condition) { }
if (condition) { } else { }
while (condition) { }
```

#### I/O

```c
print(expression);
```

#### Comments

```c
// Single line
/* Multi-line */
```

---

### Learning Path

**Beginner:**

1. Start with simple arithmetic (Example 1)
2. Learn conditionals (Example 2, 6)
3. Practice with loops (Example 3)

**Intermediate:** 4. Combine concepts (Example 4, 5) 5. Work with algorithms (Example 7, 8) 6. Study the provided examples in `examples/` folder

**Advanced:** 7. Write your own algorithms 8. Explore compiler output with `--show-ir` and `--show-asm` 9. Learn how your code becomes machine code

---

### Tips for Success

✅ **Do:**

- Declare all variables before using them
- Use meaningful variable names
- Add comments to explain your logic
- Test with simple values first
- Use `print()` to debug your programs

❌ **Don't:**

- Forget semicolons `;` at the end of statements
- Try to use variables before declaring them
- Mix types (assign `bool` to `int` or vice versa)
- Create infinite loops without planning
- Use undefined variables

---

## Compiler Phases

The MiniC compiler consists of six distinct phases:

### Phase 1: Lexical Analysis (Lexer)

Tokenizes the source code into meaningful symbols (keywords, identifiers, operators, literals).

**Output Format**: List of tokens with type and value

### Phase 2: Syntax Analysis (Parser)

Builds an Abstract Syntax Tree (AST) from tokens using recursive descent parsing.

**Output Format**: Tree structure showing program hierarchy

- Uses ASCII tree characters: `|--`, `+--`, `|   `
- Shows node types: `<Program>`, `<VarDeclaration>`, `<Assignment>`, `<BinaryExpression>`
- Displays nested structure of expressions and statements

### Phase 3: Semantic Analysis

Validates types, scopes, and variable usage with comprehensive error checking.

**Output Format**: Tree structure with semantic information

- Shows scope hierarchy with numbers (Scope 0, Scope 1, etc.)
- Displays type information for all variables
- Shows nested blocks: `<ThenBlock>`, `<ElseBlock>`, `<LoopBody>`
- Validation status: `[OK]` or `[ERROR]` with explanations

### Phase 4: Intermediate Representation (IR)

Generates Three-Address Code (TAC) - **intentionally generates extra temporaries** for educational purposes.

**Key Characteristics**:

- Creates 2-3x more instructions than necessary
- Demonstrates unoptimized intermediate form
- Each operation broken into simple steps
- Shows what optimization will improve

**Example**: Simple addition `x = a + b` becomes:

```
t0 = a
t1 = b
t2 = t0 + t1
t3 = t2
x = t3
```

### Phase 5: Optimization

Performs aggressive optimizations on the IR to eliminate redundancy.

**Optimization Techniques**:

1. **Copy Propagation**: Eliminates unnecessary assignments (if `x = y` then replace `x` with `y`)
2. **Algebraic Simplification**:
   - `x + 0` → `x`
   - `x * 1` → `x`
   - `x * 0` → `0`
3. **Strength Reduction**: Converts expensive operations to cheaper ones (e.g., `x * 2` → `x + x`)
4. **Dead Code Elimination**: Removes unused variables and assignments
5. **Iterative Optimization**: Runs up to 10 passes until no more improvements

**Results**: Typically achieves 50-70% instruction reduction

**Example**:

- Before: 49 instructions
- After: 15 instructions
- Reduction: 69.4%

### Phase 6: Code Generation

Generates **readable pseudocode assembly** (not executable machine code).

**Output Format**: Human-readable pseudocode

- Platform-independent representation
- Self-documenting operation names
- Clear control flow with labels
- Educational focus over execution

---

## Pseudocode Assembly

### Overview

Phase 6 generates **pseudocode assembly** instead of real x86-64 or ARM code. This design choice makes the compiler's output more accessible and educational.

### Why Pseudocode?

1. **Educational Value**: Students can understand the flow without learning architecture-specific assembly
2. **Readability**: Operations are self-documenting (`ADD` vs `addq`)
3. **Platform Independence**: Not tied to any specific processor architecture
4. **Focus on Concepts**: Emphasizes compiler concepts over machine details
5. **Debugging**: Much easier to trace through and understand

### Pseudocode Format

#### Program Structure

```
PROGRAM START
--------------------

[Variable declarations]
[Instructions]

--------------------
PROGRAM END
```

#### Variable Declarations

```
DECLARE variable_name
```

#### Instructions

| Instruction     | Description        | Example                        |
| --------------- | ------------------ | ------------------------------ |
| `SET`           | Assign a value     | `SET x = 42`                   |
| `ADD`           | Addition           | `SET t0 = ADD(a, b)`           |
| `SUBTRACT`      | Subtraction        | `SET t0 = SUBTRACT(a, b)`      |
| `MULTIPLY`      | Multiplication     | `SET t0 = MULTIPLY(a, b)`      |
| `DIVIDE`        | Division           | `SET t0 = DIVIDE(a, b)`        |
| `MODULO`        | Remainder          | `SET t0 = MODULO(a, b)`        |
| `NEGATE`        | Unary minus        | `SET t0 = NEGATE(x)`           |
| `LOGICAL_NOT`   | Boolean NOT        | `SET t0 = LOGICAL_NOT(flag)`   |
| `LESS_THAN`     | Comparison <       | `SET t0 = LESS_THAN(a, b)`     |
| `GREATER_THAN`  | Comparison >       | `SET t0 = GREATER_THAN(a, b)`  |
| `LESS_EQUAL`    | Comparison <=      | `SET t0 = LESS_EQUAL(a, b)`    |
| `GREATER_EQUAL` | Comparison >=      | `SET t0 = GREATER_EQUAL(a, b)` |
| `EQUAL`         | Comparison ==      | `SET t0 = EQUAL(a, b)`         |
| `NOT_EQUAL`     | Comparison !=      | `SET t0 = NOT_EQUAL(a, b)`     |
| `LOGICAL_AND`   | Boolean AND        | `SET t0 = LOGICAL_AND(a, b)`   |
| `LOGICAL_OR`    | Boolean OR         | `SET t0 = LOGICAL_OR(a, b)`    |
| `PRINT`         | Output value       | `PRINT(x)`                     |
| `GOTO`          | Unconditional jump | `GOTO L1`                      |
| `IF/THEN GOTO`  | Conditional jump   | `IF t0 == false THEN GOTO L0`  |
| `LABEL:`        | Jump target        | `L0:`                          |

### Examples

#### Simple Arithmetic

**MiniC Code:**

```c
{
    int a;
    int b;
    int sum;

    a = 15;
    b = 4;
    sum = a + b;
    print(sum);
}
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

#### Control Flow (If-Else)

**MiniC Code:**

```c
{
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
}
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

#### Loops

**MiniC Code:**

```c
{
    int counter;
    counter = 1;

    while (counter <= 5) {
        print(counter);
        counter = counter + 1;
    }
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

### Comparison: x86-64 vs Pseudocode

#### x86-64 (Before):

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

#### Pseudocode (After):

```
SET x = 10
SET y = 5
SET t0 = ADD(x, y)
SET sum = t0
```

### Usage

```bash
# Generate pseudocode assembly
python minic.py program.mc

# View the pseudocode assembly
python minic.py program.mc --show-asm

# Output to specific file
python minic.py program.mc -o myprogram.asm
```

### Implementation Notes

**Files Modified**:

1. `compiler/asmgen.py` - Complete rewrite for pseudocode generation
2. `minic.py` - Updated file extensions (.s → .asm) and user messages

**Key Design Decisions**:

- Operations use functional notation: `SET result = ADD(a, b)`
- Control flow uses high-level constructs: `IF condition THEN GOTO label`
- Variables use their original names (not registers or memory addresses)
- Labels (L0, L1, etc.) clearly show control flow structure
- Temporary variables (t0, t1, etc.) show intermediate computations

### Notes

- The pseudocode is **not executable** - it's for educational visualization only
- All optimizations from Phase 5 are visible in the output
- Labels show control flow structure clearly
- Temporary variables demonstrate intermediate computations
- To generate actual executable code, a real backend targeting a specific architecture would be needed

---

## Project Structure

```
MiniC/
├── minic.py                 # Main compiler entry point
├── web_interface.py         # Flask web interface
├── README.md                # This comprehensive documentation
├── compiler/
│   ├── __init__.py
│   ├── lexer.py            # Phase 1: Tokenization
│   ├── parser.py           # Phase 2: AST construction
│   ├── ast_nodes.py        # AST node definitions with tree printer
│   ├── semantic.py         # Phase 3: Semantic analysis with tree output
│   ├── ir_generator.py     # Phase 4: Inefficient TAC generation
│   ├── optimizer.py        # Phase 5: Aggressive IR optimization
│   └── asmgen.py           # Phase 6: Pseudocode generation
├── examples/
│   ├── hello.mc            # Simple hello world
│   ├── arithmetic.mc       # Basic arithmetic operations
│   ├── conditionals.mc     # If-else examples
│   ├── loops.mc            # While loop examples
│   ├── fibonacci.mc        # Fibonacci sequence
│   └── prime.mc            # Prime number checker
└── build/                   # Output directory (.asm files)
```

---

## Requirements

- Python 3.7 or higher
- Flask (for web interface): `pip install flask`

---

## Command-Line Options

```bash
python minic.py <source_file> [options]

Options:
  --show-tokens      Display lexical tokens (Phase 1)
  --show-ast         Display abstract syntax tree (Phase 2)
  --show-semantic    Display semantic analysis results (Phase 3)
  --show-ir          Display intermediate representation - before optimization (Phase 4)
  --show-optimized   Display optimized IR - after optimization (Phase 5)
  --show-asm         Display generated pseudocode assembly (Phase 6)
  --show-all         Display all phases
  -o, --output       Specify output file
```

### Examples

```bash
# Compile and generate output file
python minic.py examples/fibonacci.mc

# View the AST structure
python minic.py examples/fibonacci.mc --show-ast

# Compare unoptimized vs optimized IR
python minic.py examples/loops.mc --show-ir --show-optimized

# See all compiler phases
python minic.py examples/prime.mc --show-all

# Custom output file
python minic.py examples/hello.mc -o output/hello.asm
```

---

## Example Programs

| Program           | Description           | Key Features                                    | Lines |
| ----------------- | --------------------- | ----------------------------------------------- | ----- |
| `hello.mc`        | Basic hello world     | Simple print statement                          | 5     |
| `arithmetic.mc`   | Arithmetic operations | All operators, expressions                      | 20    |
| `conditionals.mc` | Conditional logic     | If-else statements, comparisons                 | 18    |
| `loops.mc`        | Looping constructs    | While loops, counters, accumulation             | 25    |
| `fibonacci.mc`    | Fibonacci sequence    | Loops with multiple variables, state management | 30    |
| `prime.mc`        | Prime number checker  | Complex logic, nested operations, algorithms    | 35    |

### Optimization Results

Example optimization improvements:

| Program         | Unoptimized IR   | Optimized IR    | Reduction |
| --------------- | ---------------- | --------------- | --------- |
| `hello.mc`      | 7 instructions   | 3 instructions  | 57%       |
| `arithmetic.mc` | 63 instructions  | 24 instructions | 62%       |
| `loops.mc`      | 105 instructions | 42 instructions | 60%       |
| `fibonacci.mc`  | 134 instructions | 54 instructions | 60%       |

---

## Web Interface

The web interface provides an interactive way to compile and explore MiniC programs:

```bash
python web_interface.py
```

Then navigate to `http://localhost:5000` in your browser.

### Features

- **Live Code Editor**: Write and edit MiniC code with syntax highlighting
- **Real-Time Compilation**: Compile instantly with the click of a button
- **Visual Phase Display**: See all six compiler phases in an organized layout
- **Example Program Selector**: Load pre-written examples to learn from
- **Tree Format Output**: Phases 2 and 3 display hierarchical tree structures
- **Optimization Comparison**: Compare unoptimized vs optimized IR side-by-side
- **Mobile Responsive**: Works on desktop, tablet, and mobile devices

### Interface Layout

1. **Editor Panel**: Write your MiniC code
2. **Control Panel**: Compile button and example selector
3. **Output Panels**: Six tabs showing each compiler phase
   - Phase 1: Tokens
   - Phase 2: AST (Tree Format)
   - Phase 3: Semantic Analysis (Tree Format)
   - Phase 4: Unoptimized IR
   - Phase 5: Optimized IR
   - Phase 6: Pseudocode Assembly

---

## Technical Details

### Lexer (Phase 1)

- Hand-written tokenizer using state machine
- Supports all MiniC tokens (keywords, identifiers, literals, operators, punctuation)
- Line and column tracking for accurate error messages
- Handles single-line (`//`) and multi-line (`/* */`) comments

### Parser (Phase 2)

- Recursive descent parser with predictive parsing
- Builds tree-structured Abstract Syntax Tree (AST)
- Comprehensive error reporting with context
- Grammar-based node construction
- Tree visualization using ASCII art (`|--`, `+--`, `|   `)

### Semantic Analyzer (Phase 3)

- Symbol table management with nested scopes
- Type checking for all operations (arithmetic, logical, comparison)
- Variable declaration and usage validation
- Scope tracking for blocks (if-else, while loops)
- Tree-format output showing scope hierarchy
- Detailed error messages with line numbers

### IR Generator (Phase 4)

- Generates Three-Address Code (TAC) from AST
- **Intentionally inefficient** design for educational demonstration
- Creates 2-3x more temporaries than necessary
- Each operation produces multiple intermediate steps
- Shows "raw" unoptimized form that benefits greatly from Phase 5

**Example inefficiency**:

```
# For simple: x = a + b
t0 = a          # Unnecessary copy
t1 = b          # Unnecessary copy
t2 = t0 + t1    # Actual operation
t3 = t2         # Unnecessary copy
x = t3          # Final assignment
```

### Optimizer (Phase 5)

- **Copy Propagation**: Eliminates redundant assignments
  - If `x = y` and `y` doesn't change, replace all uses of `x` with `y`
- **Algebraic Simplification**: Simplifies mathematical expressions
  - `x + 0` → `x`
  - `x * 1` → `x`
  - `x * 0` → `0`
  - `0 + x` → `x`
  - `1 * x` → `x`
- **Strength Reduction**: Replaces expensive operations with cheaper ones
  - `x * 2` → `x + x`
  - `x / 1` → `x`
- **Dead Code Elimination**: Removes unused variables and assignments
- **Iterative Optimization**: Runs optimizations repeatedly (up to 10 passes) until convergence
- Achieves typical instruction reduction of 50-70%

### Assembly Generator (Phase 6)

- Generates **readable pseudocode** instead of machine code
- Platform-independent, educational representation
- **Operations**: SET, ADD, SUBTRACT, MULTIPLY, DIVIDE, MODULO, PRINT
- **Comparisons**: LESS_THAN, GREATER_THAN, LESS_EQUAL, GREATER_EQUAL, EQUAL, NOT_EQUAL
- **Logical**: LOGICAL_AND, LOGICAL_OR, LOGICAL_NOT
- **Control Flow**: GOTO, IF/THEN, labels (L0, L1, etc.)
- **Format**: Human-readable with clear structure
- Not executable - designed for understanding and visualization

### Error Handling

The compiler provides detailed error messages at each phase:

**Lexical Errors**:

```
Error: Invalid character '@' at line 5, column 3
```

**Syntax Errors**:

```
Error: Expected ';' after statement at line 7
```

**Semantic Errors**:

```
Error: Variable 'count' used before declaration at line 10
Error: Type mismatch: Cannot assign bool to int at line 15
```

---

## License

MIT License - feel free to use for educational purposes.

---

## Contributing

This is an educational project. Feel free to fork and experiment!

Suggestions for enhancements:

- Add more optimization passes
- Implement constant folding
- Add data flow analysis visualization
- Create more example programs
- Add interactive tutorials
- Implement code generation for real architectures (as a learning extension)

---

## Author

Created as an educational compiler demonstration project to teach:

- Compiler design principles
- Multi-phase compilation process
- Optimization techniques
- Assembly generation concepts

**Happy Coding! 🚀**
