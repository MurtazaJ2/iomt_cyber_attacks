#include <stdio.h>

// Unsafe macro with side effects
#define SQUARE(x) x * x

int main() {
    int a = 5;
    
    // Macro side effect: a++ is evaluated twice
    int result = SQUARE(a++);
    
    printf("Result is %d\n", result);
    
    // Type mismatch and format string vulnerability
    float pi = 3.14159;
    printf("Pi is %d\n", pi); // Using %d for float
    
    return 0;
}
