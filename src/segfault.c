#include <stdio.h>

void trigger_segmentation_fault() {
    int *ptr = NULL;
    *ptr = 42; // This will cause a segmentation fault
}

int main() {
    printf("Attempting to trigger a segmentation fault...\n");
    trigger_segmentation_fault();
    printf("This line will never be reached.\n");
    return 0;
}
