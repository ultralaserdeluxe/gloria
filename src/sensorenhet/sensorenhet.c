/*
 * styrenhet.c
 *
 * Created: 2014-11-04 15:44:45
 * Description: Software for our sensorunit
 */ 

#define F_CPU 16000000UL
#define LINESENSOR_DELAY_US 10	//How long we wait before ADC
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
	bool refreshing;
} sensor_data_t;

sensor_data_t *sensors;

/* Read and save sensordata */
void read_sensors()
{
	sensors->refreshing = true;
	ADMUX = 0x67;
	PORTA = 0x00;
	_delay_us(LINESENSOR_DELAY_US);
	while(sensors->refreshing)
	{
		ADCSRA |= 1<<ADSC;		// Start Conversion
		while(ADCSRA & (1<<ADSC));
		//ADCSRA &= 0xEF;
		switch (ADMUX)
		{
		case 0x67:
			sensors->line[PORTA & 0x0F] = ADCH;
			if ((PORTA & 0x0F) >= 10)
			{
				ADMUX = 0x64;
				PORTA = 0x00;
				//ADCSRA |= 1<<ADSC;		// Start Conversion
			}
			else
			{
				PORTA = PORTA + 1;
				_delay_us(LINESENSOR_DELAY_US);
				//ADCSRA |= 1<<ADSC;		// Start Conversion
			}
			break;
		case 0x64:
			sensors->distance[0] = ADCH;
			ADMUX = 0x65;
			//ADCSRA |= 1<<ADSC;		// Start Conversion
			break;
		case 0x65:
			ADMUX = 0x67;
			sensors->distance[1] = ADCH;
			sensors->refreshing = false;
			break;
		}
	}
}


/*ADC Conversion Complete Interrupt Service Routine (ISR)
	Based on contents in ADMUX, save result from ADC to correct variable*/
ISR(ADC_vect)
{
	switch (ADMUX)
	{
	case 0x67:
		sensors->line[PORTA & 0x0F] = ADCH;
		if ((PORTA & 0x0F) >= 10)
		{
			ADMUX = 0x64;
			ADCSRA |= 1<<ADSC;		// Start Conversion
		}
		else
		{
			PORTA = PORTA + 1;
			_delay_us(LINESENSOR_DELAY_US);
			ADCSRA |= 1<<ADSC;		// Start Conversion
		}
		break;
	case 0x64:
		sensors->distance[0] = ADCH;
		ADMUX = 0x65;
		ADCSRA |= 1<<ADSC;		// Start Conversion
		break;
	case 0x65:
		sensors->distance[1] = ADCH;
		sensors->refreshing = false;
		break;
	}
}

int main(void)
{
	sensors = malloc(sizeof(sensor_data_t));
	sensors->refreshing = false;
	
	/* Configure ADC */
	DDRB = 0xFF;			// Configure PortB as output
	DDRA = 0x0F;			// Configure PortA as input
							// PA0 is ADC0 input
	
	ADCSRA = 0x88;			// Enable the ADC and its interrupt feature
							// and set the ACD clock pre-scalar to clk/128
	
	/* Configure SPI */
	//spi_slave_init();
	
	/* Enable interrupts */
	//sei();
	
	int result[8]; //DEBUG
	
	while(1)
	{
		read_sensors();
		/* DEBUG translate values (0-5 of line) to bools and put on PORTB */
		
		for (int i = 5; i < 11; i++)
		{
			if (sensors->line[i] > 0x80)
			{
				result[i - 5] = 1;
			}
			else
			{
				result[i - 5] = 0;
			}
		}
		
		if (sensors->distance[0] > 0x20) result[6] = 1;
		else result[6] = 0;
		
		if (sensors->distance[1] > 0x20) result[7] = 1;
		else result[7] = 0;
		
		//PORTB = sensors->line[1];
		//PORTB = PORTA;
		PORTB = (result[0]<<PORTB0)|(result[1]<<PORTB1)|(result[2]<<PORTB2)|(result[3]<<PORTB3)|(result[4]<<PORTB4)|(result[5]<<PORTB5)|(result[6]<<PORTB6)|(result[7]<<PORTB7);
		
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