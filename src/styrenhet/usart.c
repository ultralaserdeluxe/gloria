/*
 * usart.c
 *
 * Created: 2014-11-09
 * Description: Functions for working with USART.
 */ 


#include <avr/io.h>


void usart_init( void )
{
	
	DDRD = 0xFB; // 11111011
	/* Set baudrate */
	UBRR1H = 0x00;
	UBRR1L = 0x00;
	/* Enable receiver and transmitter */
	UCSR1B = (0<<RXEN1)|(1<<TXEN1);
	/* Set frame format: 8data, 2stop bit */
	UCSR1C = (3<<UCSZ10);
}

void usart_transmit( unsigned char data )
{
	//UCSR1B = (0<<RXEN1)|(1<<TXEN1);
	/* Wait for empty transmit buffer */
	while ( !( UCSR1A & (1<<UDRE1)) )
	;
	/* Put data into buffer, sends the data */
	UDR1 = data;
	//UCSR1B = (0<<RXEN1)|(0<<TXEN1);
}

unsigned char usart_receive( void )
{
	//UCSR1B = (1<<RXEN1)|(0<<TXEN1);
	/* Wait for data to be received */
	while ( !(UCSR1A & (1<<RXC1)) )
	;
	/* Get and return received data from buffer */
	//UCSR1B = (0<<RXEN1)|(0<<TXEN1);
	return UDR1;
}