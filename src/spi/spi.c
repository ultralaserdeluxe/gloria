/*
 * spi.c
 *
 * Created: 2014-11-06
 * Description: Functions for working with SPI.
 */ 

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <stdbool.h>
#include "spi.h"

void spi_recieve_handler(unsigned int);

ISR(SPI_STC_vect)
{
	spi_recieve_handler(SPDR);
	 //BUG SOMEWHERE BELOW ?
	 //if (!empty_SPI_transmit_queue(transmit_q))
	 //{
		 //SPDR = pop_transmit_queue_data(transmit_q);
	 //}
}

void spi_slave_init()
{
	/* Set MISO output, all others input */
	DDRB |= (1<<PORTB6);
	//DDRB &= (0<<PORTB4)|(0<<PORTB5)|(0<<PORTB7);
	/* Enable SPI */
	SPCR = (1<<SPE)|(1<<SPIE);
	
	//transmit_queue_init();
}

transmit_node_t* create_transmit_node(uint8_t data)
{
	transmit_node_t *this = malloc(sizeof(transmit_node_t));
	this->data = data;
	return this;
}

void free_transmit_node(transmit_node_t *node)
{
	free(node);
}

void add_transmit_queue(transmit_queue_t *q, uint8_t data)
{
	if (empty_SPI_transmit_queue(q))
	{
		q->first_node = create_transmit_node(data);
		q->last_node = q->first_node;
	}
	else
	{
		transmit_node_t *new_node = create_transmit_node(data);
		q->last_node->next = new_node;
		q->last_node = new_node;
	}
}

uint8_t pop_transmit_queue_data(transmit_queue_t *q)
{
	if (empty_SPI_transmit_queue(q))	return NULL;
	transmit_node_t *current = q->first_node;
	uint8_t data = q->first_node->data;
	
	q->first_node = current->next;
	if (empty_SPI_transmit_queue(q)) q->last_node = NULL;
	
	free_transmit_node(current);
	return data;
}

void transmit_queue_init()
{
	transmit_q = malloc(sizeof(transmit_queue_t));
	transmit_q->first_node = NULL;
	transmit_q->last_node = NULL;
}

bool empty_SPI_transmit_queue(transmit_queue_t *q)
{
	if (q->first_node == NULL) return true;
	else return false;
}

void spi_slave_transmit(uint8_t data)
{
	add_transmit_queue(transmit_q, data);
}
