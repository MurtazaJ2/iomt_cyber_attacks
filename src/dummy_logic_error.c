#include <stdio.h>

void process_array(int arr[]) {
    // Out of bounds array indexing
    for (int i = 0; i <= 10; i++) {
        arr[i] = i * 2;
    }
}

int main() {
    int my_array[5]; // Array of size 5
    
    process_array(my_array);
    
    // Uninitialized variable logic error
    int uninit_var;
    if (uninit_var > 0) {
        printf("Positive\n");
    }
    
    return 0;
}
