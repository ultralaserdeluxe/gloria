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
#include "usart.h"
#include "command_queue.h"

/* Global queue of received commands */
queue_t *my_queue;



int main(void)
{
	my_queue = new_queue();
	
	/* port a = output */
	DDRA = 0xFF;
		
	/* Init SPI and enable global interrupts */
	spi_slave_init();
	sei();
		
	/* Set baud to clk/16 => 1Mbps */
	usart_init();

	while(1) 
		{
		/* Set move speed */
		_delay_ms(1000);
		usart_transmit(0xFF);
		_delay_ms(1);
		usart_transmit(0xFF);
		_delay_ms(1);
		usart_transmit(0x07); //ID
		_delay_ms(1);
		usart_transmit(0x04); //Length
		_delay_ms(1);
		usart_transmit(0x04); //INstruction
		_delay_ms(1);
		usart_transmit(0x21); //Set speed
		_delay_ms(1);
		usart_transmit(0x00); //Max
		_delay_ms(1);
		usart_transmit(0xCF);	//checksum	

		/* Set goal position */
		_delay_ms(5);
		usart_transmit(0xFF);
		_delay_ms(1);
		usart_transmit(0xFF);
		_delay_ms(1);
		usart_transmit(0x07); //ID
		_delay_ms(1);
		usart_transmit(0x04); //Length
		_delay_ms(1);
		usart_transmit(0x04); //Instruction
		_delay_ms(1);
		usart_transmit(0x1E);	//Address
		_delay_ms(1);
		usart_transmit(0xFF);	//Data
		_delay_ms(1);
		usart_transmit(0xD3);

		/* Action */
		_delay_ms(5);
		usart_transmit(0xFF);
		_delay_ms(1);
		usart_transmit(0xFF);
		_delay_ms(1);
		usart_transmit(0xFE); //ID
		_delay_ms(1);
		usart_transmit(0x03); //Length
		_delay_ms(1);
		usart_transmit(0x05); //Instruction
		_delay_ms(1);
		usart_transmit(0xF9);
	};
}

void spi_recieve_handler(unsigned int data)
{
	/* Take data, put in current command. Create new if current is done.
		Perform actions if action command */
	PORTA = SPDR;
}
