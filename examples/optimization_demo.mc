// Demonstration of optimization
int x;
int y;
int result;

x = 10;
y = 5;

// These operations will be simplified by the optimizer
result = x + 0;
print(result);

result = x * 1;
print(result);

result = x * 2;  // Will become x + x
print(result);

result = y + y;
print(result);
