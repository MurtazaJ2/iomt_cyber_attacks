#include <stdio.h>
#include <string.h>

void log_message(const char *user_input) {
    // 3. Buffer Overflows & Unsafe Functions
    char local_buffer[16];

    // Unsafe string copy that could cause buffer overflow
    strcpy(local_buffer, user_input);
    
    printf("Logged: %s\n", local_buffer);
}

int main() {
    // Passing a string longer than 16 characters
    log_message("This string is significantly longer than 16 characters");
    return 0;
}
