# MiniC Compiler

A complete compiler demonstrating all six classical compiler phases with direct x86-64 assembly generation.

---

## 🚀 Quick Start (Just Want to Play?)

### 1. Compile and Run

```bash
python3 minic.py examples/fibonacci.mc
gcc build/fibonacci.s -o build/fibonacci
./build/fibonacci
```

### 2. Try All Examples

```bash
python3 minic.py examples/hello.mc && gcc build/hello.s -o build/hello && ./build/hello
python3 minic.py examples/arithmetic.mc && gcc build/arithmetic.s -o build/arithmetic && ./build/arithmetic
python3 minic.py examples/loops.mc && gcc build/loops.s -o build/loops && ./build/loops
```

### 3. Write Your Own

Create `mycode.mc`:

```c
int main() {
    int x;
    x = 10;
    while (x > 0) {
        print(x);
        x = x - 1;
    }
}
```

Run it:

```bash
python3 minic.py mycode.mc
gcc build/mycode.s -o build/mycode
./build/mycode
```

**That's it!** 🎉

**📖 New to MiniC?** [Learn the language →](LANGUAGE.md)

---

## 📚 Language Features

- **Data Types**: `int`, `bool`
- **Operators**: `+` `-` `*` `/` `%` `<` `>` `<=` `>=` `==` `!=` `&&` `||` `!`
- **Control Flow**: `if-else`, `while` loops
- **I/O**: `print(expression);`
- **Comments**: `//` single-line, `/* */` multi-line

📖 **[Learn the language →](LANGUAGE.md)** - Complete language reference with examples

## Compiler Phases

1. **Lexical Analysis**: Tokenizes source code using regex-based patterns
2. **Syntax Analysis**: Builds an Abstract Syntax Tree (AST) using recursive descent parsing
3. **Semantic Analysis**: Type checking, symbol table management, and error detection
4. **Intermediate Code Generation**: Three-Address Code (TAC) generation
5. **Optimization**: Constant folding and dead code elimination
6. **Code Generation**: Generates x86-64 assembly (direct machine code)

## 📁 Project Structure

```
MiniC/
├── compiler/           # Compiler implementation
│   ├── lexer.py       # Phase 1: Lexical Analysis
│   ├── parser.py      # Phase 2: Syntax Analysis
│   ├── ast_nodes.py   # AST definitions
│   ├── semantic.py    # Phase 3: Semantic Analysis
│   ├── ir_generator.py# Phase 4: IR Generation
│   ├── optimizer.py   # Phase 5: Optimization
│   └── asmgen.py      # Phase 6: Assembly Generation
├── examples/          # Sample programs
│   ├── hello.mc
│   ├── fibonacci.mc
│   ├── loops.mc
│   └── ...
├── build/             # Output files (auto-generated)
├── minic.py           # Compiler entry point
└── README.md
```

## 📋 Requirements

**Python 3.7+** (no external dependencies)
**GCC** (for assembling .s files to executables)

## 🎯 Command Options

```bash
python3 minic.py <file.mc> [options]
```

| Option          | Description                             |
| --------------- | --------------------------------------- |
| `-o FILE`       | Output file (default: `build/<name>.s`) |
| `--show-tokens` | Show lexical analysis (Phase 1)         |
| `--show-ast`    | Show syntax tree (Phase 2)              |
| `--show-ir`     | Show intermediate code (Phase 4)        |
| `--show-asm`    | Show assembly output (Phase 6)          |
| `--no-optimize` | Skip optimization (Phase 5)             |

### Examples

```bash
# See intermediate representation
python3 minic.py examples/loops.mc --show-ir

# See generated assembly
python3 minic.py examples/arithmetic.mc --show-asm

# See all compiler phases
python3 minic.py examples/hello.mc --show-tokens --show-ast --show-ir --show-asm
```

## 💡 Example Programs

All examples in `examples/` folder:

| File              | Description        | Output              |
| ----------------- | ------------------ | ------------------- |
| `hello.mc`        | Simple print       | `42`                |
| `arithmetic.mc`   | Math operations    | Multiple results    |
| `conditionals.mc` | If-else logic      | Conditional output  |
| `loops.mc`        | While loops        | Countdown           |
| `fibonacci.mc`    | Fibonacci sequence | `0 1 1 2 3 5 8 ...` |
| `prime.mc`        | Prime checker      | `1` or `0`          |
| `logical.mc`      | Boolean logic      | Logic results       |

### Sample Code

```c
int main() {
    int x;
    x = 10;

    while (x > 0) {
        print(x);
        x = x - 1;
    }
}
```

## 🔧 How It Works

The compiler transforms your code through 6 phases:

```
MiniC Code → Tokens → AST → Type-Checked AST → TAC → Optimized TAC → Assembly
```

- **Phase 1 (Lexer)**: Breaks code into tokens
- **Phase 2 (Parser)**: Builds syntax tree
- **Phase 3 (Semantic)**: Checks types and variables
- **Phase 4 (IR Generator)**: Creates intermediate code
- **Phase 5 (Optimizer)**: Improves code efficiency
- **Phase 6 (Assembly Gen)**: Generates x86-64 assembly

## ⚠️ Error Messages

Clear error reporting with line/column numbers:

```
Error at line 5, column 10: Undeclared variable 'x'
Error at line 8, column 15: Type mismatch: cannot assign bool to int
Error at line 12, column 5: Variable 'count' already declared in this scope
```

## 📂 Output Organization

All generated files go to `build/` folder automatically:

```
build/
├── fibonacci.s        # Assembly files
├── fibonacci          # Compiled binaries
├── hello.s
├── hello
└── ...
```

**Clean build folder:**

```bash
rm -rf build/
```

---

## 🏗️ Technical Details

<details>
<summary><b>Click to expand implementation details</b></summary>

### Compiler Architecture

```
Source Code (.mc)
    ↓
[Lexer] → Tokens
    ↓
[Parser] → AST
    ↓
[Semantic Analyzer] → Type-Checked AST
    ↓
[IR Generator] → Three-Address Code
    ↓
[Optimizer] → Optimized TAC
    ↓
[Assembly Generator] → x86-64 Assembly (.s)
    ↓
[GCC Assembler] → Executable Binary
```

### Phase Details

**Phase 1 - Lexical Analysis**

- Regex-based tokenization
- Handles keywords, operators, identifiers, literals
- Strips comments and whitespace

**Phase 2 - Syntax Analysis**

- Recursive descent parser
- Builds Abstract Syntax Tree (AST)
- Error recovery and reporting

**Phase 3 - Semantic Analysis**

- Symbol table management
- Static type checking
- Scope resolution
- Detects undeclared/redeclared variables

**Phase 4 - IR Generation**

- Three-Address Code (TAC) format
- Temporary variables for expressions
- Labels for control flow

**Phase 5 - Optimization**

- Constant folding (compile-time evaluation)
- Dead code elimination
- Control flow analysis

**Phase 6 - Code Generation**

- x86-64 assembly (AT&T syntax)
- Stack-based variable allocation
- System V AMD64 calling convention
- Position-independent code
- Uses `printf` from libc for output

### Technical Specifications

- **Target Architecture**: x86-64 (AMD64)
- **Assembly Syntax**: AT&T (GNU Assembler)
- **Platform**: Linux x86-64
- **Dependencies**: Python 3.7+, GCC (for assembly/linking)

</details>

---

## 📖 Documentation

- **[LANGUAGE.md](LANGUAGE.md)** - Complete MiniC language reference and tutorial
- **[README.md](README.md)** - This file (project overview and compiler usage)

## 📄 License

MIT License - Educational project demonstrating compiler construction principles.
