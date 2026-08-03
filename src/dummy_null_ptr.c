#include <stdio.h>
#include <stdlib.h>

void update_record(int *record) {
    // 2. Segmentation Faults & Pointer Safety
    // Dereferencing without checking for NULL
    *record = 100;
}

int main() {
    int *my_record = NULL;
    
    // Will cause a segmentation fault
    update_record(my_record);
    
    return 0;
}
