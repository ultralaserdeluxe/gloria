/*
 * sensorenhet.c
 *
 * Created: 2014-11-04
 * Description: Software for our sensor unit.
 */ 

#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdlib.h>
#include "spi.h"
#include "sensors.h"

sensor_data_t* sensors;

int main(void)
{
	sensors = sensors_init();
	
	/* Configure SPI */
	spi_slave_init();
	
	/* Enable interrupts */
	sei();
	
	/* DEBUG */
	DDRD = 0xFF;

	while(1)
	{
		read_sensors(sensors);
		PORTD = sensors->distance[0];
	}
}

void spi_recieve_handler(unsigned int data)
{	
	uint8_t address = data & 0x0F;
	
	switch(address)
	{
		case 0:
		case 1:
		case 2:
		case 3:
		case 4:
		case 5:
		case 6:
		case 7:
		case 8:
		case 9:
		case 10:
		SPDR = sensors->line[address];
		break;
		case 11:
		SPDR = sensors->distance[0];
		break;
		case 12:
		SPDR = sensors->distance[1];
		break;
		default:
		SPDR = 0xFF;
		break;
	}
}