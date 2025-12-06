# MiniC Compiler - Complete Usage Guide

## Table of Contents

- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
- [Language Syntax](#language-syntax)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Basic Compilation

```bash
# Compile a program
python3 minic.py examples/fibonacci.mc

# Outputs to: build/fibonacci.s
# Then assemble and run:
gcc build/fibonacci.s -o build/fibonacci
./build/fibonacci
```

### One-Line Execution

```bash
python3 minic.py examples/hello.mc && gcc build/hello.s -o build/hello && ./build/hello
```

---

## Command Reference

### Basic Usage

```bash
python3 minic.py <input.mc> [options]
```

### Options

| Option          | Description                                | Example                                    |
| --------------- | ------------------------------------------ | ------------------------------------------ |
| `-o FILE`       | Specify output file                        | `python3 minic.py prog.mc -o build/prog.s` |
| `--show-tokens` | Display Phase 1 output (tokens)            | `python3 minic.py prog.mc --show-tokens`   |
| `--show-ast`    | Display Phase 2 output (syntax tree)       | `python3 minic.py prog.mc --show-ast`      |
| `--show-ir`     | Display Phase 4 output (intermediate code) | `python3 minic.py prog.mc --show-ir`       |
| `--show-asm`    | Display Phase 6 output (assembly)          | `python3 minic.py prog.mc --show-asm`      |
| `--no-optimize` | Skip Phase 5 (optimization)                | `python3 minic.py prog.mc --no-optimize`   |
| `-h, --help`    | Show help message                          | `python3 minic.py -h`                      |

### Output Location

By default, output goes to `build/<filename>.s`:

- Input: `examples/fibonacci.mc` → Output: `build/fibonacci.s`
- Input: `mycode.mc` → Output: `build/mycode.s`

Specify custom output with `-o`:

```bash
python3 minic.py prog.mc -o custom/path/output.s
```

---

## Language Syntax

### Program Structure

Every MiniC program needs a `main()` function:

```c
int main() {
    // Your code here
}
```

### Variables

**Declaration:**

```c
int x;      // Integer variable
bool flag;  // Boolean variable
```

**Assignment:**

```c
x = 10;
flag = true;
```

**Note**: Variables must be declared before use!

### Data Types

- `int` - Integer numbers (e.g., 0, 42, -5)
- `bool` - Boolean values: `true` or `false`

### Operators

**Arithmetic:**

```c
x = a + b;   // Addition
x = a - b;   // Subtraction
x = a * b;   // Multiplication
x = a / b;   // Division
x = a % b;   // Modulo (remainder)
```

**Comparison:**

```c
result = x < y;   // Less than
result = x > y;   // Greater than
result = x <= y;  // Less than or equal
result = x >= y;  // Greater than or equal
result = x == y;  // Equal
result = x != y;  // Not equal
```

**Logical:**

```c
result = a && b;  // Logical AND
result = a || b;  // Logical OR
result = !a;      // Logical NOT
```

### Control Flow

**If-Else:**

```c
if (x > 0) {
    print(x);
} else {
    print(0);
}
```

**While Loop:**

```c
while (i < 10) {
    print(i);
    i = i + 1;
}
```

### Output

```c
print(expression);  // Prints integer value
```

### Comments

```c
// Single-line comment

/* Multi-line
   comment block */
```

---

## Examples

### 1. Hello World

**File: `hello.mc`**

```c
int main() {
    int greeting;
    greeting = 42;
    print(greeting);
}
```

**Run:**

```bash
python3 minic.py hello.mc
gcc build/hello.s -o build/hello
./build/hello
# Output: 42
```

### 2. Countdown Loop

**File: `countdown.mc`**

```c
int main() {
    int i;
    i = 10;

    while (i > 0) {
        print(i);
        i = i - 1;
    }
}
```

**Run:**

```bash
python3 minic.py countdown.mc
gcc build/countdown.s -o build/countdown
./build/countdown
# Output: 10 9 8 7 6 5 4 3 2 1
```

### 3. Even/Odd Checker

**File: `evenodd.mc`**

```c
int main() {
    int num;
    int remainder;

    num = 7;
    remainder = num % 2;

    if (remainder == 0) {
        print(1);  // Even
    } else {
        print(0);  // Odd
    }
}
```

### 4. Fibonacci Sequence

**File: `fib.mc`**

```c
int main() {
    int n;
    int a;
    int b;
    int temp;
    int i;

    n = 10;
    a = 0;
    b = 1;
    i = 0;

    while (i < n) {
        print(a);
        temp = a + b;
        a = b;
        b = temp;
        i = i + 1;
    }
}
```

### 5. See Compiler Phases

**Show intermediate representation:**

```bash
python3 minic.py examples/loops.mc --show-ir
```

**Show generated assembly:**

```bash
python3 minic.py examples/arithmetic.mc --show-asm
```

**Show everything:**

```bash
python3 minic.py examples/hello.mc --show-tokens --show-ast --show-ir --show-asm
```

---

## Troubleshooting

### Common Errors

#### 1. Input file not found

```
Error: Input file 'program.mc' not found
```

**Solution**: Check file path is correct and file exists.

#### 2. Undeclared variable

```
Error at line 5, column 10: Undeclared variable 'x'
```

**Solution**: Declare the variable before using it:

```c
int x;  // Add this line
x = 10;
```

#### 3. Type mismatch

```
Error at line 8, column 15: Type mismatch: cannot assign bool to int
```

**Solution**: Ensure variable types match:

```c
int x;
x = 10;      // OK: int = int
x = true;    // ERROR: int = bool

bool flag;
flag = true; // OK: bool = bool
```

#### 4. Variable already declared

```
Error at line 12, column 5: Variable 'count' already declared in this scope
```

**Solution**: Each variable can only be declared once:

```c
int count;    // First declaration - OK
int count;    // ERROR: Already declared
```

#### 5. Missing semicolon

```
Parse error at line 7: Expected ';'
```

**Solution**: Add semicolon after statements:

```c
int x
x = 10  // Missing semicolons

// Should be:
int x;
x = 10;
```

### File Organization Issues

**Problem**: Too many files in main directory

**Solution**: The compiler automatically puts output in `build/` folder.

**Clean up:**

```bash
rm -rf build/  # Remove all generated files
```

### Assembly/Linking Errors

**Problem**: `gcc: command not found`

**Solution**: Install GCC:

```bash
sudo apt install gcc  # Ubuntu/Debian
```

**Problem**: Assembly warnings about stack

**Solution**: These are normal warnings, your program still works! The compiler includes proper stack notes.

---

## Advanced Usage

### Custom Output Directory

```bash
# Put output in specific location
python3 minic.py program.mc -o myoutput/program.s
gcc myoutput/program.s -o myoutput/program
```

### Batch Compilation

Compile all examples:

```bash
for file in examples/*.mc; do
    name=$(basename "$file" .mc)
    python3 minic.py "$file"
    gcc "build/$name.s" -o "build/$name"
done
```

### Compare Optimized vs Unoptimized

```bash
# With optimization (default)
python3 minic.py program.mc --show-ir > optimized.txt

# Without optimization
python3 minic.py program.mc --no-optimize --show-ir > unoptimized.txt

# Compare
diff optimized.txt unoptimized.txt
```

### Pipeline Testing

Save each phase output:

```bash
python3 minic.py program.mc --show-tokens > tokens.txt
python3 minic.py program.mc --show-ast > ast.txt
python3 minic.py program.mc --show-ir > ir.txt
python3 minic.py program.mc --show-asm > asm.txt
```

---

## File Extensions Reference

| Extension | Description       | Human Readable?                    |
| --------- | ----------------- | ---------------------------------- |
| `.mc`     | MiniC source code | ✅ Yes                             |
| `.s`      | Assembly code     | ⚠️ Somewhat (if you know assembly) |
| (none)    | Executable binary | ❌ No (machine code)               |

**Compilation flow:**

```
program.mc  →  build/program.s  →  build/program
 (source)       (assembly)          (binary)
```

---

## Tips & Best Practices

1. **Start Simple**: Begin with `examples/hello.mc` to verify setup
2. **Use --show-ir**: Great for understanding code transformation
3. **Check Assembly**: Use `--show-asm` to see generated code
4. **Keep build/ folder**: Don't commit it to git (already in .gitignore)
5. **Declare first**: Always declare variables before using them
6. **Match types**: int variables for numbers, bool for true/false
7. **Add semicolons**: Every statement needs one

---

## Quick Command Cheatsheet

```bash
# Basic compile and run
python3 minic.py examples/fibonacci.mc
gcc build/fibonacci.s -o build/fibonacci
./build/fibonacci

# Show IR (intermediate code)
python3 minic.py examples/loops.mc --show-ir

# Show assembly
python3 minic.py examples/arithmetic.mc --show-asm

# Show all phases
python3 minic.py examples/hello.mc --show-tokens --show-ast --show-ir --show-asm

# Without optimization
python3 minic.py examples/conditionals.mc --no-optimize

# Custom output
python3 minic.py mycode.mc -o custom/mycode.s

# Clean build folder
rm -rf build/
```

---

## Need Help?

Check the main [README.md](README.md) for overview and technical details.

**Common Issues:**

- Syntax errors → Check semicolons and braces
- Type errors → Match variable types
- Undeclared variables → Declare before use
- File not found → Check paths and file existence
