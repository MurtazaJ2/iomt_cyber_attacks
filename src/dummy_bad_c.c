#include <stdio.h>
#include <string.h>

void vulnerable_function(char *input) {
    char buffer[10];
    // Dangerous function that can cause a buffer overflow
    strcpy(buffer, input);
    printf("Copied to buffer: %s\n", buffer);
}

int main() {
    printf("Running bad C code...\n");
    vulnerable_function("This string is way too long for the buffer and will overflow");
    return 0;
}
