// Prime Number Checker
// Checks if a number is prime

int num;
int divisor;
int isPrime;
int remainder;

num = 29;  // Number to check
isPrime = 1;  // Assume prime (true)
divisor = 2;

// Check divisors from 2 to num-1
while (divisor < num) {
    remainder = num % divisor;
    
    if (remainder == 0) {
        isPrime = 0;  // Not prime
        divisor = num;  // Exit loop
    }
    
    divisor = divisor + 1;
}

// Print result (1 if prime, 0 if not)
print(isPrime);

// Test with another number
int num2;
int div2;
int prime2;
int rem2;

num2 = 20;
prime2 = 1;
div2 = 2;

while (div2 < num2) {
    rem2 = num2 % div2;
    if (rem2 == 0) {
        prime2 = 0;
        div2 = num2;
    }
    div2 = div2 + 1;
}

print(prime2);  // Should print 0 (not prime)
