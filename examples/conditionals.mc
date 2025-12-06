// Conditional Statements Example
// Demonstrates if-else statements

int x;
int y;
int max;

x = 42;
y = 17;

// Find maximum using if-else
if (x > y) {
    max = x;
} else {
    max = y;
}

print(max);  // 42

// Nested conditionals
if (x > 10) {
    if (y > 10) {
        print(1);  // Both greater than 10
    } else {
        print(2);  // Only x greater than 10
    }
} else {
    print(3);  // x not greater than 10
}

// Multiple conditions
int a;
a = 5;

if (a < 10) {
    if (a > 0) {
        print(100);  // a is between 0 and 10
    }
}
