/*
 * usart.c
 *
 * Created: 2014-11-09
 * Description: Functions for working with USART.
 */ 

#include <avr/io.h>

void usart_init( void )
{
	/* Set tx as output. */
	DDRD |= (1<<PORTD3);
	/* Set rx as input */
	DDRD &= 0xFB;
	
	/*disconnect rx/tx ports*/
	DDRB |= 0x03;
	PORTB |= 0x03;

	/* Set baudrate */
	UBRR1H = 0x00;
	UBRR1L = 0x00;
	/* Enable receiver and transmitter */
	UCSR1B = (1<<RXEN1)|(1<<TXEN1);
	/* Set frame format: 8data, 2stop bit */
	UCSR1C = (3<<UCSZ10);
	
	// Todo: /* We want timer so we dont get stuck while waiting for UART response */
	TCCR0A	= 0x00; /* OC0A/B as normal, no waveform generation */
	TCCR0B	= (1<<CS02)|(1<<CS00); /* Prescaler clk/1024. */
	TIMSK0  = 0x00; /* No interrupts on this timer */
	OCR0A   = 0xff; /* Should (hopefully) give a timeout of 1/61s = ~16ms. */
}

void usart_transmit( unsigned char data )
{
	/* Wait for empty transmit buffer */
	while ( !( UCSR1A & (1<<UDRE1)) )
	;
	/* Put data into buffer, sends the data */
	UDR1 = data;
}

unsigned char usart_receive( void )
{
	/* Reset counter and counter-flag */
	TCNT0 = 0x00;
	TIFR0 = (1<<OCF0A);
	/* Wait for data to be received */
	while ( !(UCSR1A & (1<<RXC1)) )
	{
		/* If time out, return NULL */
		if (OCF0A == 1) return 0;
	}
	/* Get and return received data from buffer */
	return UDR1;
}

void usart_set_tx(){
	/* Turn off rx */
	PORTB |= 0x01; //00000001
	/* Turn on tx */
	PORTB &= 0xFD; //11111101
}

void usart_set_rx(){
	/* Wait for data to be shifted out */
	while ( !( UCSR1A & (1<<TXC1)) && !( UCSR1A & (1<<UDRE1)) );
	UCSR1A |= (1<<TXC1); // Reset flag
	/* Turn off tx */
	PORTB |= 0x02; //00000010
	/* Turn on rx */
	PORTB &= 0xFE; //11111110
}

void usart_disconnect(){
	/* Wait for data to be shifted out */
	while ( !( UCSR1A & (1<<TXC1)) );
	PORTB |= 0x03; //00000011
}