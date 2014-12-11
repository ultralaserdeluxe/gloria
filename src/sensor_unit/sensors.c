/*
 * sensors.c
 *
 * Created: 2014-11-14
 * Description: Functions for working with the sensors.
 */

#include <stdlib.h>
#include <avr/io.h>
#include "sensors.h"

uint8_t adc_convert()
{
	/* Start conversion. */
	ADCSRA |= (1<<ADSC);

	/* Wait for conversion to complete. */
	while(ADCSRA & (1<<ADSC));

	return ADCH;
}

void read_linesensor(sensor_data_t* sensor_data)
{
	/* Select line sensor input. */
	ADMUX = 0x67;

	uint8_t channel;
	for(channel = line_sensor_first; channel < line_sensor_last; channel++){
		PORTA = channel & 0x0F;
		sensor_data->line[channel] = adc_convert();
	}
}

void read_distance_left(sensor_data_t* sensor_data)
{
	/* Select left distance sensor input. */
	ADMUX = 0x65;

	sensor_data->distance[0] = adc_convert();
}

void read_distance_right(sensor_data_t* sensor_data)
{
	/* Select right distance sensor input. */
	ADMUX = 0x64;

	sensor_data->distance[1] = adc_convert();
}

/* Read and save sensor data */
void read_sensors(sensor_data_t* sensor_data)
{
	read_linesensor(sensor_data);
	read_distance_left(sensor_data);
	read_distance_right(sensor_data);
}

sensor_data_t* sensors_init(){
	/* Mux address pins as outputs. */
	DDRA = 0x0F;

	/* Configure ADC */
	ADCSRA = 0x87;

	sensor_data_t* sensor_data = malloc(sizeof(sensor_data_t));

	return sensor_data;
}
