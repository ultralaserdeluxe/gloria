/*
 * usart.h
 *
 * Created: 2014-11-09
 * Description: Functions for working with USART.
 */ 


#ifndef USART_H_
#define USART_H_


void usart_init();
void usart_transmit(unsigned char data);
unsigned char usart_receive();


#endif /* USART_H_ */