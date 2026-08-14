#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef PACKET_INFO_H
#define PACKET_INFO_H

// Define a structure to hold packet information
typedef struct {
  char src_ip[46];  // Increased size to accommodate IPv6 addresses
  char dst_ip[46];  // Increased size to accommodate IPv6 addresses
  uint16_t src_port;
  uint16_t dst_port;
} packet_info;

/**
 * Initialize packet information.
 *
 * @param packet Pointer to the packet_info structure.
 */
void init_packet_info(packet_info *packet);

/**
 * Set source IP address.
 *
 * @param packet Pointer to the packet_info structure.
 * @param ip     Source IP address.
 */
void set_src_ip(packet_info *packet, const char *ip);

/**
 * Set destination IP address.
 *
 * @param packet Pointer to the packet_info structure.
 * @param ip     Destination IP address.
 */
void set_dst_ip(packet_info *packet, const char *ip);

/**
 * Set source port.
 *
 * @param packet Pointer to the packet_info structure.
 * @param port   Source port number.
 */
void set_src_port(packet_info *packet, uint16_t port);

/**
 * Set destination port.
 *
 * @param packet Pointer to the packet_info structure.
 * @param port   Destination port number.
 */
void set_dst_port(packet_info *packet, uint16_t port);

/**
 * Print packet information.
 *
 * @param packet Pointer to the packet_info structure.
 */
void print_packet_info(packet_info *packet);

/**
 * Free packet information.
 *
 * @param packet Pointer to the packet_info structure.
 */
void free_packet_info(packet_info *packet);

#endif  // PACKET_INFO_H

void init_packet_info(packet_info *packet) {
  if (packet == NULL) {
    fprintf(stderr, "Error: Packet info is NULL\n");
    return;
  }
  memset(packet->src_ip, 0, sizeof(packet->src_ip));
  memset(packet->dst_ip, 0, sizeof(packet->dst_ip));
  packet->src_port = 0;
  packet->dst_port = 0;
}

void set_src_ip(packet_info *packet, const char *ip) {
  if (packet == NULL || ip == NULL) {
    fprintf(stderr, "Error: Packet info or IP is NULL\n");
    return;
  }
  if (strlen(ip) >= sizeof(packet->src_ip)) {
    fprintf(stderr, "Error: Source IP address too long\n");
    return;
  }
  strncpy(packet->src_ip, ip, sizeof(packet->src_ip) - 1);
  packet->src_ip[sizeof(packet->src_ip) - 1] = '\0';
}

void set_dst_ip(packet_info *packet, const char *ip) {
  if (packet == NULL || ip == NULL) {
    fprintf(stderr, "Error: Packet info or IP is NULL\n");
    return;
  }
  if (strlen(ip) >= sizeof(packet->dst_ip)) {
    fprintf(stderr, "Error: Destination IP address too long\n");
    return;
  }
  strncpy(packet->dst_ip, ip, sizeof(packet->dst_ip) - 1);
  packet->dst_ip[sizeof(packet->dst_ip) - 1] = '\0';
}

void set_src_port(packet_info *packet, uint16_t port) {
  if (packet == NULL) {
    fprintf(stderr, "Error: Packet info is NULL\n");
    return;
  }
  if (port < 0 || port > 65535) {
    fprintf(stderr, "Error: Invalid source port number\n");
    return;
  }
  packet->src_port = port;
}

void set_dst_port(packet_info *packet, uint16_t port) {
  if (packet == NULL) {
    fprintf(stderr, "Error: Packet info is NULL\n");
    return;
  }
  if (port < 0 || port > 65535) {
    fprintf(stderr, "Error: Invalid destination port number\n");
    return;
  }
  packet->dst_port = port;
}

void print_packet_info(packet_info *packet) {
  if (packet == NULL) {
    fprintf(stderr, "Error: Packet info is NULL\n");
    return;
  }
  printf("Source IP: %s\n", packet->src_ip);
  printf("Destination IP: %s\n", packet->dst_ip);
  printf("Source Port: %u\n", packet->src_port);
  printf("Destination Port: %u\n", packet->dst_port);
}

void free_packet_info(packet_info *packet) {
  if (packet != NULL) {
    free(packet);
  }
}

int main() {
  packet_info *packet = malloc(sizeof(packet_info));
  if (packet == NULL) {
    fprintf(stderr, "Error: Memory allocation failed\n");
    return 1;
  }

  init_packet_info(packet);
  set_src_ip(packet, "192.168.1.100");
  set_dst_ip(packet, "8.8.8.8");
  set_src_port(packet, 1234);
  set_dst_port(packet, 80);

  print_packet_info(packet);

  free_packet_info(packet);
  return 0;
}