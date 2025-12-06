# MiniC Language Reference

Complete guide to learning and writing programs in the MiniC programming language.

---

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [Basic Syntax](#basic-syntax)
3. [Data Types](#data-types)
4. [Variables](#variables)
5. [Operators](#operators)
6. [Control Flow](#control-flow)
7. [Input/Output](#inputoutput)
8. [Comments](#comments)
9. [Complete Examples](#complete-examples)
10. [Language Limitations](#language-limitations)

---

## Introduction

MiniC is a simple, C-like programming language designed for learning compiler concepts. It's statically typed with a minimal but complete feature set.

### Your First Program

```c
int main() {
    print(42);
}
```

Every MiniC program must have a `main()` function that returns `int`. This is where your program starts executing.

---

## Basic Syntax

### Program Structure

```c
int main() {
    // Your code here
}
```

- Every program starts with `int main()`
- Code blocks are wrapped in `{ }` braces
- Statements end with semicolons `;`
- Case-sensitive: `main` is different from `Main`

### Whitespace

MiniC ignores extra whitespace (spaces, tabs, newlines), so you can format your code for readability:

```c
int main() {
    int x;
    x = 10;
    print(x);
}
```

is the same as:

```c
int main(){int x;x=10;print(x);}
```

---

## Data Types

MiniC has two data types:

### 1. Integer (`int`)

Whole numbers, positive or negative.

```c
int x;
x = 42;        // Positive
x = -15;       // Negative
x = 0;         // Zero
```

**Range**: Standard 32-bit integers (-2,147,483,648 to 2,147,483,647)

### 2. Boolean (`bool`)

True or false values.

```c
bool flag;
flag = true;
flag = false;
```

**Note**: In output, `true` displays as `1` and `false` displays as `0`.

---

## Variables

### Declaration

Variables must be declared before use:

```c
int age;           // Declare integer
bool isActive;     // Declare boolean
```

### Assignment

After declaration, you can assign values:

```c
int count;
count = 10;        // Assign 10 to count

bool ready;
ready = true;      // Assign true to ready
```

### Multiple Variables

```c
int x;
int y;
int z;

x = 5;
y = 10;
z = x + y;         // z becomes 15
```

### Variable Names (Identifiers)

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
int, bool, true, false, if, else, while, main
```

---

## Operators

### Arithmetic Operators

For `int` types only:

| Operator | Operation      | Example  | Result |
| -------- | -------------- | -------- | ------ |
| `+`      | Addition       | `5 + 3`  | `8`    |
| `-`      | Subtraction    | `5 - 3`  | `2`    |
| `*`      | Multiplication | `5 * 3`  | `15`   |
| `/`      | Division       | `10 / 3` | `3`    |
| `%`      | Modulo         | `10 % 3` | `1`    |

```c
int main() {
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

### Comparison Operators

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
int main() {
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

### Logical Operators

For `bool` types:

| Operator | Operation | Example           | Result  |
| -------- | --------- | ----------------- | ------- |
| `&&`     | AND       | `true && false`   | `false` |
| `\|\|`   | OR        | `true \|\| false` | `true`  |
| `!`      | NOT       | `!true`           | `false` |

```c
int main() {
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

### Operator Precedence

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

## Control Flow

### If-Else Statements

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
int main() {
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
int main() {
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
int main() {
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
int main() {
    int x;
    x = 15;

    if (x > 10) {
        if (x < 20) {
            print(1);    // x is between 10 and 20
        }
    }
}
```

### While Loops

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
int main() {
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
int main() {
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
int main() {
    while (true) {
        print(1);    // This will run forever!
    }
}
```

---

## Input/Output

### Print Statement

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
int main() {
    int x;
    x = 42;

    print(x);          // Prints: 42
    print(100);        // Prints: 100
    print(x + 10);     // Prints: 52
    print(x * 2);      // Prints: 84
}
```

```c
int main() {
    bool flag;
    flag = true;

    print(flag);       // Prints: 1 (true)

    flag = false;
    print(flag);       // Prints: 0 (false)
}
```

**Note**: Each `print()` outputs a number followed by a newline.

---

## Comments

Comments are ignored by the compiler and help document your code.

### Single-Line Comments

Use `//` for single-line comments:

```c
int main() {
    // This is a comment
    int x;        // Comments can be at end of line
    x = 42;       // Assign 42 to x
    print(x);
}
```

### Multi-Line Comments

Use `/* */` for multi-line comments:

```c
int main() {
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

## Complete Examples

### Example 1: Simple Calculator

```c
int main() {
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

### Example 2: Even or Odd

```c
int main() {
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

### Example 3: Factorial

```c
int main() {
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

### Example 4: Fibonacci Sequence

```c
int main() {
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

### Example 5: Prime Number Checker

```c
int main() {
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

### Example 6: Maximum of Two Numbers

```c
int main() {
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

### Example 7: Sum of Digits

```c
int main() {
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

### Example 8: Power Function

```c
int main() {
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

## Language Limitations

Understanding what MiniC **cannot** do:

### ❌ No Functions (except main)

```c
// ✗ This doesn't work
int add(int a, int b) {
    return a + b;
}
```

Only the `main()` function is allowed.

### ❌ No Arrays

```c
// ✗ This doesn't work
int numbers[10];
```

You must use separate variables.

### ❌ No Strings

```c
// ✗ This doesn't work
print("Hello World");
```

Only integer and boolean values can be printed.

### ❌ No User Input

```c
// ✗ This doesn't work
int x;
x = read();
```

All values must be hardcoded or calculated.

### ❌ No Pointers or References

```c
// ✗ This doesn't work
int* ptr;
```

### ❌ No Floating Point

```c
// ✗ This doesn't work
float x;
x = 3.14;
```

Only integers are supported.

### ❌ No Break or Continue

```c
// ✗ This doesn't work
while (true) {
    if (x > 10) {
        break;
    }
}
```

Use conditional logic instead.

### ❌ No For Loops

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

### ❌ No Switch Statements

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

## Quick Reference Card

### Keywords

```
int, bool, true, false, if, else, while, main, print
```

### Data Types

```c
int x;      // Integer
bool flag;  // Boolean
```

### Operators

```c
+  -  *  /  %              // Arithmetic
<  >  <=  >=  ==  !=       // Comparison
&&  ||  !                   // Logical
```

### Control Flow

```c
if (condition) { }
if (condition) { } else { }
while (condition) { }
```

### I/O

```c
print(expression);
```

### Comments

```c
// Single line
/* Multi-line */
```

---

## Learning Path

**Beginner:**

1. Start with simple arithmetic (Example 1)
2. Learn conditionals (Example 2, 6)
3. Practice with loops (Example 3)

**Intermediate:** 4. Combine concepts (Example 4, 5) 5. Work with algorithms (Example 7, 8) 6. Study the provided examples in `examples/` folder

**Advanced:** 7. Write your own algorithms 8. Explore compiler output with `--show-ir` and `--show-asm` 9. Learn how your code becomes machine code

---

## Tips for Success

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
- Forget the `main()` function

---

## Need Help?

- Check [README.md](README.md) for compiler usage and options
- Look at `examples/` folder for working programs
- Use `--show-tokens` and `--show-ast` to understand parsing
- Try the web interface at http://localhost:5000

**Happy Coding! 🚀**
