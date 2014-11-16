/*
 * spi.h
 *
 * Created: 2014-11-06
 * Description: Functions for working with SPI.
 */ 

#ifndef SPI_H_
#define SPI_H_

#include <stdbool.h>

typedef struct transmit_node
{
	uint8_t data;
	struct transmit_queue *next;
} transmit_node_t;

typedef struct transmit_queue
{
	transmit_node_t *first_node;
	transmit_node_t *last_node;
} transmit_queue_t;

transmit_queue_t *transmit_q;

void spi_slave_init();

transmit_node_t* create_transmit_node(uint8_t data);
void free_transmit_node(transmit_node_t *node);
void add_transmit_queue(transmit_queue_t *q, uint8_t data);
uint8_t pop_transmit_queue_data(transmit_queue_t *q);
void transmit_queue_init();
bool empty_SPI_transmit_queue(transmit_queue_t *q);

void spi_slave_transmit(uint8_t data);

#endif /* SPI_H_ */