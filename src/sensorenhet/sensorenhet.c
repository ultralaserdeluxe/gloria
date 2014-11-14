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


int main(void)
{
	sensor_data_t* sensors = sensors_init();
	
	/* Configure SPI */
	spi_slave_init();
	
	/* Enable interrupts */
	sei();
	
	/* DEBUG */
	DDRB = 0xFF;
	PORTB = 0x00;
	uint8_t result; //DEBUG	
	while(1)
	{
		read_sensors(sensors);
		result = (sensors->distance[0] & 0xF0) | ((sensors->distance[1] >> 4) & 0x0F);
		PORTB = result;
	}
}

/* UNTESTED */
void spi_recieve_handler(unsigned int data)
{
	/*
	switch(data>>4)
	{
	case 0:
		switch(data & 0x0F)
		{
		case 0:
			for (int i = 0; i < 11; i++)
			{
				spi_slave_transmit(sensors->line[i]);
			}
			break;
		case 2:
			spi_slave_transmit(sensors->distance[0]);
			break;
		case 3:
			spi_slave_transmit(sensors->distance[1]);
			break;
		case 15:
			for (int i = 0; i < 11; i++)
			{
				spi_slave_transmit(sensors->line[i]);
			}
			spi_slave_transmit(sensors->distance[0]);
			spi_slave_transmit(sensors->distance[1]);
			break;
		default:
			break;
		}
	case 1:
		break;
	case 0xFF:
		break;
	default:
		break;
	}
	*/
}