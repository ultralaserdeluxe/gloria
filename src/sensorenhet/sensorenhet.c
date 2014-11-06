/*
 * styrenhet.c
 *
 * Created: 2014-11-04 15:44:45
 *  Author: Hannes
 */ 


#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

/*ADC Conversion Complete Interrupt Service Routine (ISR)*/
ISR(ADC_vect)
{
	PORTD = ADCH;		// Output ADCH to PORTD (for debug purposes, ADCH should be saved)
	ADCSRA |= 1<<ADSC;		// Start Conversion
}

int main(void)
{
	
	DDRD = 0xFF;			// Configure PortD as output
	DDRA = 0x00;			// Configure PortA as input
							// PA0 is ADC0 input
	
	ADCSRA = 0x8F;			// Enable the ADC and its interrupt feature
							// and set the ACD clock pre-scalar to clk/128
	ADMUX = 0xE0;			// Select internal 2.56V as Vref, left justify
							// data registers and select ADC0 as input channel
	
	sei();				// Enable Global Interrupts
	ADCSRA |= 1<<ADSC;		// Start Conversion
	
    while(1);
}