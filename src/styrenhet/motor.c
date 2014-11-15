/*
 * motor.c
 *
 * Created: 2014-11-14
 * Description: Functions for motor control.
 */


#include <avr/io.h>
#include "motor.h"


void motor_init(){
	/* Set PORTA0 and PORTA1 (direction control) as output. */
	DDRA |= (1<<PORTA0)|(1<<PORTA1);
	
	/* Set PORTD6 and PORTD7 (motor PWM) as output. */	
	DDRD |= (1<<PORTD6)|(1<<PORTD7);
	
	/* Set up timer 2. */
	TCCR2A  = (1<<COM2A1); /* Clear compare register A on match. */
	TCCR2A |= (1<<COM2B1); /* Clear compare register B on match. */
	TCCR2A |= (1<<WGM20);  /* Phase correct PWM. */
	
	TCCR2B = (1<<CS20);    /* No prescaling. */
		
	/* Set initial speed to 0. */
	set_speed(0);
	
	/* Set initial direction to FORWARD. */
	set_direction(FORWARD);
}

	
void set_speed(uint8_t speed){
	OCR2A = OCR2B = speed;
}
	
	
void set_speed_left(uint8_t speed){
	OCR2A = speed;
}


void set_speed_right(uint8_t speed){
	OCR2B = speed;
}


void set_direction(direction_t direction){
	switch(direction){
		case FORWARD:
		PORTA |= 0x02;
		PORTA &= 0xFE;
		break;
		case BACKWARD:
		PORTA |= 0x01;
		PORTA &= 0xFD;		
		break;
		case ROTATE_LEFT:
		PORTA &= 0xFC;
		break;
		case ROTATE_RIGHT:
		PORTA |= 0x03;
		break;
		default:
		break;
	}
}
