﻿/*
 * usart.h
 *
 * Created: 2014-11-09
 * Description: Functions for working with USART.
 */ 


#ifndef USART_H_
#define USART_H_

#include <stdbool.h>

void usart_init();
void usart_transmit(unsigned char data);
unsigned char usart_receive();
void usart_set_tx();
void usart_set_rx();
void usart_disconnect();
void usart_flush_rx();

#endif /* USART_H_ */