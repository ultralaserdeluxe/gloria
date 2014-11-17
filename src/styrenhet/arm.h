/*
 * arm.h
 *
 * Created: 2014-11-08 14:59:51
 * Description: Functions for handling our arm.
 */ 
#ifndef ARM_H_
#define ARM_H_

#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include <avr/io.h>
#include "ax12a.h"
#include "servo.h"

/* Following datatypes stores current and goal speed/position of our servos.
	Meant to allow us to keep track of if the servo is moving and let us ramp 
	moving speed at run time. Currently not used. */
typedef struct servo_data
{
	uint8_t ID;
	uint8_t status;
	uint8_t speed_h;
	uint8_t speed_l;
	uint8_t position_h;
	uint8_t position_l;
	uint8_t goal_speed_h;
	uint8_t goal_speed_l;
	uint8_t goal_position_h;
	uint8_t goal_position_l;
} servo_data_t;

typedef struct arm_data
{
	servo_data_t *s;
	int length;
} arm_data_t;

/* Core functions for arm */
void arm_init(int servo);
void update_servo(arm_data_t *d, int address);
void update_servo_regs(arm_data_t *d, int address);
void arm_action(int address);

/* Functions for arm_data */
arm_data_t* new_arm_data(int number_of_servos);
void free_arm_data(arm_data_t *arm);
void set_servo_speed(arm_data_t *arm, int servo, uint8_t new_speed_h, uint8_t new_speed_l);
void set_servo_position(arm_data_t *arm, int servo, uint8_t new_position_h, uint8_t new_position_l);
uint16_t get_servo_speed(arm_data_t *arm, int servo);
uint16_t get_servo_position(arm_data_t *arm, int servo);
void set_servo_goal_speed(arm_data_t *arm, int servo, uint8_t new_speed_h, uint8_t new_speed_l);
void set_servo_goal_position(arm_data_t *arm, int servo, uint8_t new_position_h, uint8_t new_position_l);
uint16_t get_servo_goal_speed(arm_data_t *arm, int servo);
uint16_t get_servo_goal_position(arm_data_t *arm, int servo);

/* Unrelated */
uint16_t make_int_16(uint8_t high, uint8_t low);

void set_inverse_servo_goal_position(arm_data_t *arm, int servo, uint8_t new_speed_h, uint8_t new_speed_l);

#endif /* ARM_H_ */