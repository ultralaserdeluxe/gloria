/*
 * motor.h
 *
 * Created: 2014-11-14
 * Description: Functions for motor control.
 */ 


#ifndef MOTOR_H_
#define MOTOR_H_

#define MOTOR_LEFT 0x00
#define MOTOR_RIGHT 0x01
#define MOTOR_ALL 0x0D //Could be anything

#include <stdio.h>
#include <stdlib.h>

typedef enum {FORWARD, BACKWARD} direction_t;

typedef struct wheel_data
{
	uint8_t ID;
	direction_t direction;
	uint8_t speed;
	direction_t goal_direction;
	uint8_t goal_speed;
	direction_t queued_direction;
	uint8_t queued_speed;
} wheel_data_t;

typedef struct motor_data
{
	wheel_data_t *s;
	int length;
} motor_data_t;

void motor_init();
motor_data_t* new_motor_data(int number_of_motors);
void motor_action(int ID, motor_data_t *d);
void set_goal_velocity_left(motor_data_t *d, uint8_t direction, uint8_t speed);
void set_goal_velocity_right(motor_data_t *d, uint8_t direction, uint8_t speed);
void set_queued_velocity_left(motor_data_t *d, uint8_t direction, uint8_t speed);
void set_queued_velocity_right(motor_data_t *d, uint8_t direction, uint8_t speed);

void set_speed_left(uint8_t speed);
void set_speed_right(uint8_t speed);
void set_direction_left(direction_t direction);
void set_direction_right(direction_t direction);

#endif /* MOTOR_H_ */