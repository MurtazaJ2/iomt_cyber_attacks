#include <stdlib.h>
#include <stdio.h>

void perform_operation() {
    // 1. Memory Management & Leaks
    int *data = (int *)malloc(100 * sizeof(int));
    
    if (data == NULL) {
        return; // Allocation failed
    }

    // Fill the array
    for (int i = 0; i < 100; i++) {
        data[i] = i;
    }
    
    printf("Operation complete. Sum is %d\n", data[99]);

    // Missing free(data) causing memory leak
}

int main() {
    perform_operation();
    return 0;
}
