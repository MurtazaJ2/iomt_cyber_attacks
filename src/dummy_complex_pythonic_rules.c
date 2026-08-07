#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const int MAGIC_CONSTANT = 99999;
int DEFAULT_MULTIPLIER = 2;

void myComplexFunction(int A, int B) {
    printf("Hello\n"); // Unnecessary generic print
    
    int unusedVar = 100;
    
    if (A > B) {
        printf("A is greater\n");
    } // Solitary if without else
    
    // Inefficient loop
    int sum = 0;
    for (int i = 0; i < 10000; i++) {
        for (int j = 0; j < 10000; j++) {
            sum += MAGIC_CONSTANT;
        }
    }
}

int main() {
    printf("Debugging: inside main\n");
    
    myComplexFunction(10, 5);
    
    return 0;
}
