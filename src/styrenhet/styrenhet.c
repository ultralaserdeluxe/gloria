/*
 * styrenhet.c
 *
 * Created: 2014-11-06
 * Description: Main file.
 */ 


#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include "spi.h"


ISR(SPI_STC_vect)
{
	/* send to pins of PORTA */
	PORTA = SPDR;
}


int main(void)
{
	/* port a = output */ 
	DDRA = 0xFF; 
	
	spi_slave_init();
	
	/* enable global interrupts */ 
	sei();

    while(1)
    {

    }
}