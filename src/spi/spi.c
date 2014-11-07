/*
 * spi.c
 *
 * Created: 2014-11-06
 * Description: Functions for working with SPI.
 */ 


#include <avr/io.h>


void spi_slave_init()
{
	/* Set MISO output, all others input */
	DDRB = (1<<PORTB6);
	/* Enable SPI */
	SPCR = (1<<SPE)|(0<<MSTR)|(1<<SPIE);
}
