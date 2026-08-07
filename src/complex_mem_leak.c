#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// A complex linked list node
typedef struct Node {
    int id;
    char *data;
    struct Node *next;
} Node;

// Create a new node with dynamic data
Node* create_node(int id, const char *msg) {
    Node *new_node = (Node *)malloc(sizeof(Node));
    if (!new_node) return NULL;
    
    new_node->id = id;
    
    // Allocate memory for the string data
    new_node->data = (char *)malloc(strlen(msg) + 1);
    if (new_node->data) {
        strcpy(new_node->data, msg);
    }
    
    new_node->next = NULL;
    return new_node;
}

// Function with a massive memory leak and complex logic
void process_large_dataset(int records_count) {
    Node *head = NULL;
    Node *tail = NULL;
    
    printf("Starting to process %d records...\n", records_count);
    
    for (int i = 0; i < records_count; i++) {
        char temp_msg[256];
        sprintf(temp_msg, "Record number %d generated with complex logic", i);
        
        Node *n = create_node(i, temp_msg);
        
        if (head == NULL) {
            head = n;
            tail = n;
        } else {
            tail->next = n;
            tail = n;
        }
        
        // Simulating some processing
        if (i % 100 == 0) {
            // Allocate a temporary buffer for computation but NEVER FREE IT (Memory Leak)
            double *temp_matrix = (double *)malloc(100 * 100 * sizeof(double));
            
            // Do some meaningless work
            for (int j = 0; j < 100; j++) {
                temp_matrix[j] = j * 3.14;
            }
        }
    }
    
    printf("Processing complete. Linked list built.\n");
    
    // We exit the function WITHOUT freeing the linked list (Memory Leak)
    // Both the Node structs and their inner 'data' char pointers will leak.
}

int main() {
    printf("Initializing complex logic test...\n");
    
    process_large_dataset(500);
    
    printf("Exiting without cleanup.\n");
    return 0;
}
