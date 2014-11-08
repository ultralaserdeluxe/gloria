/*
 * styrenhet.c
 *
 * Created: 2014-11-06
 * Description: Main file.
 */ 

#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "spi.h"
#include "command_queue.h"

/* Global queue of recieved commands */
queue_t *my_queue;

ISR(SPI_STC_vect)
{
	/* send to pins of PORTA */
	PORTA = SPDR;
}

int main(void)
{
	my_queue = new_queue();
	
	/* port a = output */
	DDRA = 0xFF;
		
	/* Init SPI and enable global interrupts */
	spi_slave_init();
	sei();
		
	/* Set baud to clk/16 => 1Mbps */
	USART_init();

	while(1) 
		{
		/* Set move speed */
		_delay_ms(1000);
		USART_Transmit(0xFF);
		_delay_ms(1);
		USART_Transmit(0xFF);
		_delay_ms(1);
		USART_Transmit(0x07); //ID
		_delay_ms(1);
		USART_Transmit(0x04); //Length
		_delay_ms(1);
		USART_Transmit(0x04); //INstruction
		_delay_ms(1);
		USART_Transmit(0x21); //Set speed
		_delay_ms(1);
		USART_Transmit(0x00); //Max
		_delay_ms(1);
		USART_Transmit(0xCF);	//checksum	

		/* Set goal position */
		_delay_ms(5);
		USART_Transmit(0xFF);
		_delay_ms(1);
		USART_Transmit(0xFF);
		_delay_ms(1);
		USART_Transmit(0x07); //ID
		_delay_ms(1);
		USART_Transmit(0x04); //Length
		_delay_ms(1);
		USART_Transmit(0x04); //Instruction
		_delay_ms(1);
		USART_Transmit(0x1E);	//Address
		_delay_ms(1);
		USART_Transmit(0xFF);	//Data
		_delay_ms(1);
		USART_Transmit(0xD3);

		/* Action */
		_delay_ms(5);
		USART_Transmit(0xFF);
		_delay_ms(1);
		USART_Transmit(0xFF);
		_delay_ms(1);
		USART_Transmit(0xFE); //ID
		_delay_ms(1);
		USART_Transmit(0x03); //Length
		_delay_ms(1);
		USART_Transmit(0x05); //Instruction
		_delay_ms(1);
		USART_Transmit(0xF9);
	};
}

void handle_spi(unsigned int data)
{
	/* Take data, put in current command. Create new if current is done.
		Perform actions if action command */
}

void USART_init( void )
{
	/* Set baudrate */
	UBRR1H = 0x00;
	UBRR1L = 0x00;
	/* Enable receiver and transmitter */
	UCSR1B = (0<<RXEN1)|(1<<TXEN1);
	/* Set frame format: 8data, 2stop bit */
	UCSR1C = (1<<USBS1)|(3<<UCSZ10);
}

void USART_Transmit( unsigned char data )
{
	/* Wait for empty transmit buffer */
	while ( !( UCSR1A & (1<<UDRE1)) )
	;
	/* Put data into buffer, sends the data */
	UDR1 = data;
}

unsigned char USART_Receive( void )
{
	/* Wait for data to be received */
	while ( !(UCSR1A & (1<<RXC1)) )
	;
	/* Get and return received data from buffer */
	return UDR1;
}