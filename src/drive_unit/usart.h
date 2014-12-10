/*
* usart.h
*
* Created: 2014-11-09
* Description: Functions for working with USART.
*/


#ifndef USART_H_
#define USART_H_

#include <stdbool.h>
#include "parameter_chain.h"

typedef struct usart_buffer
{
	servo_parameter_t *head;
	servo_parameter_t *tail;
} usart_buffer_t;

usart_buffer_t usart_receive_buffer;

void usart_init();
void usart_transmit(unsigned char data);
unsigned char usart_receive( void );
void usart_recieve_buffer_init();
bool usart_is_buffer_empty();
void usart_put_recieve(unsigned char in);
unsigned char usart_pop_recieve( void );
void usart_flush_rx();
void usart_set_tx();
void usart_set_rx();
void usart_disconnect();
#endif /* USART_H_ */
