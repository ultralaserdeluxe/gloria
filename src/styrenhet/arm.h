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

/* The following datatypes are meant to be a readable list of commands to be 
	forwarded to the specified servo */

typedef struct command_struct
{
	uint8_t instruction;
	servo_parameter_t *first_parameter;
	
	/* Comparing status with expected length of recieved message
		tells us whether we have recieved the whole message */
	int status;
} command_struct_t;

typedef struct command_queue_node
{
	command_struct_t *command;
	struct command_queue_node *next;
} command_queue_node_t;

typedef struct command_queue
{
	command_queue_node_t *head;
	command_queue_node_t *last;
} command_queue_t;

/* Core functions for arm */
command_queue_t* arm_init(int servo);
void do_action(int address, command_queue_t *q);

/* The following functions are really good to have */
servo_instruction_t* command_to_arm_instr(command_struct_t *c);

/* Functions for queue */
command_queue_t* new_queue();
void free_queue(command_queue_t *q);
void put_queue(command_queue_t *q, command_queue_node_t *node);
command_queue_node_t* pop_first(command_queue_t *q);
void remove_node(command_queue_t *q, command_queue_node_t *node);
bool empty_queue(command_queue_t *this);

/* Functions for queue_node */
command_queue_node_t* first_node(command_queue_t *this);
command_queue_node_t* last_node(command_queue_t *this);
command_queue_node_t* next_node(command_queue_node_t *node);
command_queue_node_t* new_node();
command_queue_node_t* free_node(command_queue_node_t* this);
command_struct_t* node_data(command_queue_node_t *node);
int set_node_command(command_queue_node_t *node, int chooser, int data);

/* Functions for command */
int set_command(command_struct_t *command, int chooser, uint8_t data);
command_struct_t* new_command();
int command_status(command_struct_t current);

/* Following datatypes stores current and goal speed/position of our servos.
	Meant to allow us to keep track of if the servo is moving and let us ramp 
	moving speed at run time. Currently not used. */
typedef struct servo_data
{
	unsigned int speed;
	unsigned int position;
	unsigned int goal_speed;
	unsigned int goal_position;
	uint8_t error;
} servo_data_t;

typedef struct arm_data
{
	servo_data_t *s;
	int length;
} arm_data_t;

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

#endif /* ARM_H_ */