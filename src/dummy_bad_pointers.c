#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void use_dangling_pointer() {
    char *ptr = (char *)malloc(20 * sizeof(char));
    strcpy(ptr, "Hello World!");
    
    // Freeing the memory
    free(ptr);
    
    // Using the dangling pointer
    printf("String after free: %s\n", ptr);
}

void uninitialized_pointer() {
    int *uninit_ptr;
    
    // Dereferencing an uninitialized pointer
    *uninit_ptr = 100;
    
    printf("Value: %d\n", *uninit_ptr);
}

int main() {
    use_dangling_pointer();
    uninitialized_pointer();
    return 0;
}
