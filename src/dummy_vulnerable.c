#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Missing docstrings and parameter explanations
void process_data(char *input)
{
    // 1. Buffer Overflows & Unsafe Functions
    char buffer[10];
    strcpy(buffer, input); // UNSAFE: strcpy
    
    char msg[20];
    sprintf(msg, "Processed: %s", buffer); // UNSAFE: sprintf

    // 2. Segmentation Faults & Pointer Safety
    int *uninit_ptr;
    *uninit_ptr = 42; // Uninitialized pointer dereference

    // 3. Memory Management & Leaks
    char *leak_ptr = (char *)malloc(100);
    strcpy(leak_ptr, "This will leak");
    // No free(leak_ptr);

    char *use_after_free = (char *)malloc(50);
    free(use_after_free);
    strcpy(use_after_free, "Use after free"); // Use-after-free

    // 4. Undefined Behavior & Arithmetic Safety
    int uninit_var;
    int result = uninit_var + 10; // Uninitialized variable

    int zero = 0;
    int div_zero = 100 / zero; // Division by zero
    
    // 5. Resource Management
    FILE *fp = fopen("dummy_file.txt", "r");
    if(fp != NULL) {
        // solitary if, no fclose
        char line[256];
        gets(line); // UNSAFE: gets
    }

    // 6. C Coding Standards & Style
    int camelCaseVar = 10; // Inconsistent naming
    int A = 5;
    
    // 7. Code Optimization & Best Practices
    for (int i=0; i<100; i++) {
        int redundant = i * 2; // redundant calculation / dead code
    }
}

int main() {
    process_data("This input is way too long for a 10 byte buffer and will cause an overflow");
    return 0;
}
