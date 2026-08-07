#include <stdio.h>
#include <string.h>

void buffer_overflow_example() {
    char small_buffer[5];
    char large_string[] = "This is a very long string that will overflow the small buffer.";
    
    // Using strcpy which is unsafe
    strcpy(small_buffer, large_string);
    
    printf("Buffer contains: %s\n", small_buffer);
}

void out_of_bounds_array() {
    int numbers[10];
    
    // Writing out of bounds
    for (int i = 0; i <= 15; i++) {
        numbers[i] = i * i;
    }
    
    printf("Finished writing to array.\n");
}

int main() {
    buffer_overflow_example();
    out_of_bounds_array();
    return 0;
}
