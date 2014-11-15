/*
 * motor.c
 *
 * Created: 2014-11-14
 * Description: Functions for motor control.
 * Todo: set_speed capable of taking motor_data_t and setting motors accordingly
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

motor_data_t* new_motor_data(int number_of_motors)
{
	motor_data_t *this = malloc(sizeof(motor_data_t));
	this->length = number_of_motors;
	this->s = malloc(number_of_motors * sizeof(wheel_data_t));
	return this;
}

void motor_action(int ID, motor_data_t *d)
{
	switch (ID)
	{
	case MOTOR_ALL:
		set_goal_speed_left(d, d->s[MOTOR_LEFT].queued_direction, d->s[MOTOR_LEFT].queued_speed);
		set_goal_speed_right(d, d->s[MOTOR_RIGHT].queued_direction, d->s[MOTOR_RIGHT].queued_speed);
		break;
	case MOTOR_LEFT:
		set_goal_speed_left(d, d->s[MOTOR_LEFT].queued_direction, d->s[MOTOR_LEFT].queued_speed);
		break;
	case MOTOR_RIGHT:
		set_goal_speed_right(d, d->s[MOTOR_RIGHT].queued_direction, d->s[MOTOR_RIGHT].queued_speed);
		break;
	default:
		/* Unreachable statement */
		break;
	}
}

void set_goal_speed_left(motor_data_t *d, uint8_t direction, uint8_t speed)
{
	d->s[MOTOR_LEFT].goal_direction = direction;
	d->s[MOTOR_LEFT].goal_speed = speed;
}

void set_goal_speed_right(motor_data_t *d, uint8_t direction, uint8_t speed)
{
	d->s[MOTOR_RIGHT].goal_direction = direction;
	d->s[MOTOR_RIGHT].goal_speed = speed;
}

void set_queued_speed_left(motor_data_t *d, uint8_t direction, uint8_t speed)
{
	d->s[MOTOR_LEFT].queued_direction = direction;
	d->s[MOTOR_LEFT].queued_speed = speed;
}

void set_queued_speed_right(motor_data_t *d, uint8_t direction, uint8_t speed)
{
	d->s[MOTOR_RIGHT].queued_direction = direction;
	d->s[MOTOR_RIGHT].queued_speed = speed;
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
