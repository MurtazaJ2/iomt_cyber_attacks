#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define a constant for the maximum buffer size
#define MAX_BUFFER_SIZE 1024

// Function to handle memory allocation errors
void handle_allocation_error(const char *message) {
    fprintf(stderr, "Memory allocation error: %s\n", message);
    exit(EXIT_FAILURE);
}

// Function to handle file operation errors
void handle_file_error(const char *message) {
    fprintf(stderr, "File operation error: %s\n", message);
    exit(EXIT_FAILURE);
}

// Function to safely copy a string
char *safe_string_copy(const char *source) {
    if (source == NULL) {
        handle_allocation_error("Source string is null");
    }
    size_t length = strlen(source);
    char *destination = malloc(length + 1);
    if (destination == NULL) {
        handle_allocation_error("Failed to allocate memory for string copy");
    }
    strncpy(destination, source, length + 1);
    destination[length] = '\0'; // Ensure null-termination
    return destination;
}

// Function to safely concatenate two strings
char *safe_string_concat(const char *str1, const char *str2) {
    if (str1 == NULL || str2 == NULL) {
        handle_allocation_error("Source strings are null");
    }
    size_t length = strlen(str1) + strlen(str2) + 1;
    char *result = malloc(length);
    if (result == NULL) {
        handle_allocation_error("Failed to allocate memory for string concatenation");
    }
    snprintf(result, length, "%s%s", str1, str2);
    return result;
}

// Function to safely read a line from a file
char *safe_read_line(FILE *file) {
    if (file == NULL) {
        handle_file_error("File pointer is null");
    }
    char *line = malloc(MAX_BUFFER_SIZE);
    if (line == NULL) {
        handle_allocation_error("Failed to allocate memory for reading line");
    }
    if (fgets(line, MAX_BUFFER_SIZE, file) == NULL) {
        free(line);
        handle_file_error("Failed to read line from file");
    }
    // Check if the line is null-terminated
    if (line[strlen(line) - 1] != '\n') {
        // Line is not null-terminated, reallocate memory
        size_t length = strlen(line);
        char *new_line = realloc(line, length + 1);
        if (new_line == NULL) {
            handle_allocation_error("Failed to reallocate memory for reading line");
        }
        new_line[length] = '\0'; // Ensure null-termination
        line = new_line;
    }
    return line;
}

int main() {
    // Open a file for reading
    FILE *file = fopen("src/dummy_bad_c.c", "r");
    if (file == NULL) {
        handle_file_error("Failed to open file for reading");
    }

    // Read a line from the file
    char *line = safe_read_line(file);

    // Close the file
    if (fclose(file) != 0) {
        free(line);
        handle_file_error("Failed to close file");
    }

    // Print the read line
    printf("%s", line);

    // Free allocated memory
    free(line);

    return EXIT_SUCCESS;
}