// Logical Operations Example
// Demonstrates boolean variables and logical operators

bool a;
bool b;
bool result;

// Test AND operator
a = true;
b = true;
if (a && b) {
    print(1);  // Both true
}

a = true;
b = false;
if (a && b) {
    print(2);  // Won't print
} else {
    print(3);  // Will print
}

// Test OR operator
a = false;
b = false;
if (a || b) {
    print(4);  // Won't print
} else {
    print(5);  // Will print
}

a = false;
b = true;
if (a || b) {
    print(6);  // Will print (at least one true)
}

// Test NOT operator
a = true;
if (!a) {
    print(7);  // Won't print
} else {
    print(8);  // Will print
}

// Complex logical expressions
int x;
int y;
x = 10;
y = 20;

if ((x < y) && (x > 0)) {
    print(100);  // Will print
}

if ((x > y) || (y > 15)) {
    print(200);  // Will print (second condition is true)
}

// Combining comparisons and logical operators
if ((x < 50) && (y < 50) && (x > 0)) {
    print(300);  // Will print
}
