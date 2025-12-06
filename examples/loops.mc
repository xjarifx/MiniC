// Loop Examples
// Demonstrates while loops

int counter;
int sum;

// Simple counting loop
counter = 1;
while (counter <= 5) {
    print(counter);  // 1, 2, 3, 4, 5
    counter = counter + 1;
}

// Sum of numbers from 1 to 10
counter = 1;
sum = 0;
while (counter <= 10) {
    sum = sum + counter;
    counter = counter + 1;
}
print(sum);  // 55

// Powers of 2
int power;
power = 1;
while (power < 1000) {
    print(power);  // 1, 2, 4, 8, 16, 32, 64, 128, 256, 512
    power = power * 2;
}

// Countdown
counter = 10;
while (counter > 0) {
    print(counter);  // 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
    counter = counter - 1;
}
