// Fibonacci Sequence
// Calculates and prints first N Fibonacci numbers

int n;
int a;
int b;
int temp;
int i;

n = 15;  // Number of Fibonacci numbers to generate
a = 0;
b = 1;
i = 0;

print(a);  // First Fibonacci number

while (i < n) {
    print(b);
    temp = a + b;
    a = b;
    b = temp;
    i = i + 1;
}

/* Expected output:
   0
   1
   1
   2
   3
   5
   8
   13
   21
   34
   55
   89
   144
   233
   377
   610
*/
