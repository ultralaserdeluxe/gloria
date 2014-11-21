/*
 * motor.c
 *
 * Created: 2014-11-14
 * Description: Functions for motor control.
 * Todo: set_speed capable of taking motor_data_t and setting motors accordingly
 */


#include <avr/io.h>
#include <avr/interrupt.h>
#include "motor.h"
#include "styrenhet.h"

void motor_init()
{
	/* Set PORTA0 and PORTA1 (direction control) as output. */
	DDRA |= (1<<PORTA0)|(1<<PORTA1);

	/* Set up timer 2 for PWM generation. */
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
	
	
	/* Set up timer 1 (16-bit) for acceleration control. */
	TCCR1B  = (1<<WGM22); /* CTC mode. */
	TCCR1B |= (1<<CS22)|(1<<CS20); /* Prescaler clk/1024. */
	TIMSK1  = (1<<OCIE1A); /* Enable interrupt on OCR1A */
	OCR1A   = 1562; /* Should give an update period of ~10 Hz. */
}

ISR(TIMER1_COMPA_vect)
{
	/* Left motor. */
	uint8_t current_speed_left = gloria_queue->motor->s[MOTOR_LEFT].speed;
	uint8_t goal_speed_left = gloria_queue->motor->s[MOTOR_LEFT].goal_speed;
	uint8_t current_direction_left = gloria_queue->motor->s[MOTOR_LEFT].direction;
	uint8_t goal_direction_left = gloria_queue->motor->s[MOTOR_LEFT].goal_direction;
	
	if(current_direction_left == goal_direction_left)
	{
		uint8_t new_left_speed = current_speed_left + ((goal_speed_left - current_speed_left) / 2);
		gloria_queue->motor->s[MOTOR_LEFT].speed = new_left_speed;
		set_speed_left(new_left_speed);
	}else if(current_speed_left < 0x10){
		gloria_queue->motor->s[MOTOR_LEFT].direction = goal_direction_left;
		set_direction_left(goal_direction_left);
	}else{
		uint8_t new_left_speed = current_speed_left - (current_speed_left / 3);
		gloria_queue->motor->s[MOTOR_LEFT].speed = new_left_speed;
		set_speed_left(new_left_speed);
	}
	
	/* Right motor. */
	uint8_t current_speed_right = gloria_queue->motor->s[MOTOR_RIGHT].speed;
	uint8_t goal_speed_right = gloria_queue->motor->s[MOTOR_RIGHT].goal_speed;
	uint8_t current_direction_right = gloria_queue->motor->s[MOTOR_RIGHT].direction;
	uint8_t goal_direction_right = gloria_queue->motor->s[MOTOR_RIGHT].goal_direction;
		
	if(current_direction_right == goal_direction_right)
	{
		uint8_t new_right_speed = current_speed_right + ((goal_speed_right - current_speed_right) / 2);
		gloria_queue->motor->s[MOTOR_RIGHT].speed = new_right_speed;
		set_speed_right(new_right_speed);
		}else if(current_speed_right < 0x10){
		gloria_queue->motor->s[MOTOR_RIGHT].direction = goal_direction_right;
		set_direction_right(goal_direction_right);
		}else{
		uint8_t new_right_speed = current_speed_right - (current_speed_right / 3);
		gloria_queue->motor->s[MOTOR_RIGHT].speed = new_right_speed;
		set_speed_right(new_right_speed);
	}
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
	
void set_speed_left(uint8_t speed)
{
	OCR2A = speed;
}

void set_speed_right(uint8_t speed)
{
	OCR2B = speed;
}

void set_direction_left(direction_t direction)
{
	switch(direction)
	{
		case FORWARD:
			PORTA |= 0x01;
			break;
		case BACKWARD:
			PORTA &= 0xFE; 
			break;
		default:
			break;
	}
}

void set_direction_right(direction_t direction)
{
	switch(direction)
	{
		case FORWARD:
			PORTA &= 0xFE;	
			break;
		case BACKWARD:
			PORTA |= 0x01;
			break;
		default:
			break;
	}
}