/*
 * spi.c
 *
 * Created: 2014-11-06
 * Description: Functions for working with SPI.
 */ 


#ifndef spi_h__
#define spi_h__

#include <avr/io.h>
#include <avr/interrupt.h>


void spi_recieve_handler(unsigned int);


ISR(SPI_STC_vect)
{
	spi_recieve_handler(SPDR);
}


void spi_slave_init()
{
	/* Set MISO output, all others input */
	DDRB = (1<<PORTB6);
	/* Enable SPI */
	SPCR = (1<<SPE)|(0<<MSTR)|(1<<SPIE);
}
#endif // spi_h__
