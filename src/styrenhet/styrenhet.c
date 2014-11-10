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


int main(void)
{	
	/* port a = output */
	DDRA = 0xFF;
		
	/* Init SPI and enable global interrupts */
	spi_slave_init();
	sei();
	
	DDRD = 0xFF;
	TCCR2A = (1<<COM2A1)|(1<<COM2B1)|(1<<WGM20);
	TCCR2B = (0<<WGM22)|(0<<CS21)|(1<<CS20);
	
	OCR2A = OCR2B = 0x00;
	
	PORTA = 0x81; // set dir

	uint8_t speed;
	
	while(1) 
	{
		for(speed = 0; speed < 250; speed++){
			OCR2A = OCR2B = speed;
			_delay_ms(10);
		}
		for(; speed > 0; speed--){
			OCR2A = OCR2B = speed;
			_delay_ms(10);
		}
	};
}

void spi_recieve_handler(unsigned int data)
{
	/* Take data, put in current command. Create new if current is done.
		Perform actions if action command */
	PORTA = data;
}
