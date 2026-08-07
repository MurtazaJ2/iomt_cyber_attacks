#include <stdio.h>

void do_something() {
    int val = 42;
    printf("Value: %d\n", val) // Missing semicolon
}

int main() {
    do_something();
    return 0;
}
