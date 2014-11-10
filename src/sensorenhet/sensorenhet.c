/*
 * styrenhet.c
 *
 * Created: 2014-11-04 15:44:45
 * Description: Software for our sensorunit
 */ 

#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <stdbool.h>
#include <stdlib.h>
#include "spi.h"

typedef struct sensor_data
{
	uint8_t line[11];
	uint8_t distance[2];
} sensor_data_t;

sensor_data_t *sensors;

/*ADC Conversion Complete Interrupt Service Routine (ISR)*/
ISR(ADC_vect)
{
	switch (ADMUX)
	{
	case 0x63:
		//PORTB = PORTA;
		sensors->line[PORTA>>4] = ADCH;
		break;
	case 0x60:
		sensors->distance[0] = ADCH;
		break;
	case 0x61:
		sensors->distance[1] = ADCH;
		break;
	}
	//PORTD = ADCH;		// Output ADCH to PORTD (for debug purposes, ADCH should be saved)
}

int main(void)
{
	sensors = malloc(sizeof(sensor_data_t));
	
	/* Configure ADC */
	//DDRB = 0xFF;			// Configure PortB as output
	DDRA = 0xF0;			// Configure PortA as input
							// PA0 is ADC0 input
	
	ADCSRA = 0x8F;			// Enable the ADC and its interrupt feature
							// and set the ACD clock pre-scalar to clk/128
	ADMUX = 0x63;			// Select internal 2.56V as Vref, left justify
							// data registers and select ADC0 as input channel
	
	/* Configure SPI */
	spi_slave_init();
	
	/* Enable interrupts */
	sei();
	
	//int result[8]; //DEBUG
	
    while(1)
	{
		ADMUX = 0x63;	//Choose linesensor ADC
		for (uint8_t i = 0; i < 11; i++)
		{
			PORTA = i<<4;
			_delay_ms(5);
			ADCSRA |= 1<<ADSC;		// Start Conversion
			_delay_ms(10);
		}
		ADMUX = 0x60; //Choose distance1
		ADCSRA |= 1<<ADSC;		// Start Conversion
		_delay_ms(10);
		
		ADMUX = 0x61; //Choose distance1
		ADCSRA |= 1<<ADSC;		// Start Conversion
		_delay_ms(10);
		
		/* DEBUG translate values (0-5 of line) to bools and put on PORTB */
		/*for (int i = 0; i < 6; i++)
		{
			if (sensors->line[i] > 0x80)
			{
				result[i] = 1;
			}
			else
			{
				result[i] = 0;
			}
		}
		
		if (sensors->distance[0] > 0x20) result[6] = 1;
		else result[6] = 0;
		
		if (sensors->distance[1] > 0x20) result[7] = 1;
		else result[7] = 0;
		
		PORTB = (result[0]<<PORTB0)|(result[1]<<PORTB1)|(result[2]<<PORTB2)|(result[3]<<PORTB3)|(result[4]<<PORTB4)|(result[5]<<PORTB5)|(result[6]<<PORTB6)|(result[7]<<PORTB7);
		*/
	}
}

/* UNTESTED */
void spi_recieve_handler(unsigned int data)
{
	switch(data>>4)
	{
	case 0:
		/* Return requested data */
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
		/* Calibrate sensor */
		break;
	case 0xFF:
		/* Transmit slave data */
		break;
	default:
		break;
	}
}