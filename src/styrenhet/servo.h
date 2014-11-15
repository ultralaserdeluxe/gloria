/*
 * armlib.h
 *
 * Created: 2014-11-08 17:52:50
 * Description: Functions for arm.
 */ 

#ifndef ARMLIB_H_
#define ARMLIB_H_

#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>

typedef struct servo_data
{
	unsigned int speed;
	unsigned int position;
	unsigned int goal_speed;
	unsigned int goal_position;
} servo_data_t;

typedef struct arm_data
{
	servo_data_t *s;
	int length;
} arm_data_t;

typedef struct parameter
{
	unsigned int current_parameter;
	struct parameter *next;
} parameter_t;

/* Represents a command recieved from DAD
	Contains data to be sent to arm to perform said command */
typedef struct arm_instruction
{
	parameter_t *first_parameter;
	parameter_t *last_parameter;
	/* Number of parameters */
	int length;
} arm_instruction_t;

arm_data_t* new_arm_data(int number_of_servos);
void free_arm_data(arm_data_t *arm);
void set_servo_speed(arm_data_t *arm, int servo, unsigned int new_speed);
void set_servo_position(arm_data_t *arm, int servo, unsigned int new_position);
int get_servo_speed(arm_data_t *arm, int servo);
int get_servo_position(arm_data_t *arm, int servo);
void set_servo_goal_speed(arm_data_t *arm, int servo, unsigned int new_speed);
void set_servo_goal_position(arm_data_t *arm, int servo, unsigned int new_position);
int get_servo_goal_speed(arm_data_t *arm, int servo);
int get_servo_goal_position(arm_data_t *arm, int servo);

arm_instruction_t* create_instructions(int amount);
arm_instruction_t* concatenate_instructions(arm_instruction_t *t1, arm_instruction_t *t2);
void free_instruction(arm_instruction_t *t);
void free_instruction_full(arm_instruction_t *t);
void add_parameter(arm_instruction_t *instr, unsigned int new_parameter);
parameter_t* get_parameter(arm_instruction_t *instr);
parameter_t* next_parameter(parameter_t *p);
parameter_t* create_parameter(unsigned int new_parameter);
bool empty_parameter(parameter_t *p);
parameter_t* last_parameter(parameter_t *p);
unsigned int parameter_value(parameter_t *p);

#endif /* ARMLIB_H_ */