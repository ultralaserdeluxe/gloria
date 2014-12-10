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
#include <math.h>


void new_motor_data(int number_of_motors)
{
	motor.length = number_of_motors;
	motor.s = malloc(number_of_motors * sizeof(wheel_data_t));
}

void motor_init()
{

	for (int i = 0; i <= motor.length; i++)
	{
		motor.s[i].ID = i;
		motor.s[i].goal_speed = 0;
		motor.s[i].goal_direction = 0;
	}

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

	/* Set up timer 1 (16-bit) for acceleration control. */
	TCCR1B  = (1<<WGM22); /* CTC mode. */
	TCCR1B |= (1<<CS22)|(1<<CS20); /* Prescaler clk/1024. */
	TIMSK1  = (1<<OCIE1A); /* Enable interrupt on OCR1A */
	OCR1A   = 1562; /* Should give an update period of ~10 Hz. */
}

ISR(TIMER1_COMPA_vect)
{
	/* Left motor. */
	uint8_t current_speed_left = motor.s[MOTOR_LEFT].speed;
	uint8_t goal_speed_left = motor.s[MOTOR_LEFT].goal_speed;
	uint8_t current_direction_left = motor.s[MOTOR_LEFT].direction;
	uint8_t goal_direction_left = motor.s[MOTOR_LEFT].goal_direction;

	//if(current_direction_left == goal_direction_left)
	//{
		//uint8_t new_left_speed = current_speed_left + ((goal_speed_left - current_speed_left) / 2);
		//gloria_queue->motor->s[MOTOR_LEFT].speed = new_left_speed;
		//set_speed_left(new_left_speed);
	//}
	//else if(current_speed_left < 0x10)
	//{
		//gloria_queue->motor->s[MOTOR_LEFT].direction = goal_direction_left;
		//set_direction_left(goal_direction_left);
	//}
	//else
	//{
		//uint8_t new_left_speed = current_speed_left - (current_speed_left / 3);
		//gloria_queue->motor->s[MOTOR_LEFT].speed = new_left_speed;
		//set_speed_left(new_left_speed);
	//}
	//
	/* Right motor. */
	uint8_t current_speed_right = motor.s[MOTOR_RIGHT].speed;
	uint8_t goal_speed_right = motor.s[MOTOR_RIGHT].goal_speed;
	uint8_t current_direction_right = motor.s[MOTOR_RIGHT].direction;
	uint8_t goal_direction_right = motor.s[MOTOR_RIGHT].goal_direction;

	//if(current_direction_right == goal_direction_right)
	//{
		//uint8_t new_right_speed = current_speed_right + ((goal_speed_right - current_speed_right) / 2);
		//gloria_queue->motor->s[MOTOR_RIGHT].speed = new_right_speed;
		//set_speed_right(new_right_speed);
	//}
	//else if(current_speed_right < 0x10)
	//{
		//gloria_queue->motor->s[MOTOR_RIGHT].direction = goal_direction_right;
		//set_direction_right(goal_direction_right);
	//}
	//else
	//{
		//uint8_t new_right_speed = current_speed_right - (current_speed_right / 3);
		//gloria_queue->motor->s[MOTOR_RIGHT].speed = new_right_speed;
		//set_speed_right(new_right_speed);
	//}

	/* Temp function w/o acceleration */
	set_speed_left(goal_speed_left);
	set_speed_right(goal_speed_right);
	set_direction_left(goal_direction_left);
	set_direction_right(goal_direction_right);
}

void motor_action(int ID)
{
	switch (ID)
	{
	case MOTOR_ALL:
		set_goal_velocity_left(motor.s[MOTOR_LEFT].queued_direction, motor.s[MOTOR_LEFT].queued_speed);
		set_goal_velocity_right(motor.s[MOTOR_RIGHT].queued_direction, motor.s[MOTOR_RIGHT].queued_speed);
		break;
	case MOTOR_LEFT:
		set_goal_velocity_left(motor.s[MOTOR_LEFT].queued_direction, motor.s[MOTOR_LEFT].queued_speed);
		break;
	case MOTOR_RIGHT:
		set_goal_velocity_right(motor.s[MOTOR_RIGHT].queued_direction, motor.s[MOTOR_RIGHT].queued_speed);
		break;
	default:
		/* Unreachable statement */
		break;
	}
}

void set_goal_velocity_left(direction_t direction, uint8_t speed)
{
	motor.s[MOTOR_LEFT].goal_direction = direction;
	motor.s[MOTOR_LEFT].goal_speed = speed;
}

void set_goal_velocity_right(direction_t direction, uint8_t speed)
{
	motor.s[MOTOR_RIGHT].goal_direction = direction;
	motor.s[MOTOR_RIGHT].goal_speed = speed;
}

void set_queued_velocity_left(direction_t direction, uint8_t speed)
{
	motor.s[MOTOR_LEFT].queued_direction = direction;
	motor.s[MOTOR_LEFT].queued_speed = speed;
}

void set_queued_velocity_right(direction_t direction, uint8_t speed)
{
	motor.s[MOTOR_RIGHT].queued_direction = direction;
	motor.s[MOTOR_RIGHT].queued_speed = speed;
}

void set_speed_left(uint8_t speed)
{
	OCR2B = speed;
}

void set_speed_right(uint8_t speed)
{
	OCR2A = speed;
}

void set_direction_left(direction_t direction)
{
	switch(direction)
	{
		case FORWARD:
			PORTA |= 0x02;
			break;
		case BACKWARD:
			PORTA &= 0xFD;
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
