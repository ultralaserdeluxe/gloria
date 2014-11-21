/*
 * command_queue.h
 *
 * Created: 2014-11-15 16:28:28
 *	Description: Command queue takes command bytes and makes arm/motors perform
 *					Requested actions.
 */ 

#ifndef COMMAND_QUEUE_H_
#define COMMAND_QUEUE_H_

#define COMMAND_STATUS_LENGTH_OFFSET 0x03

#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include <avr/io.h>
#include "ax12a.h"
#include "huvud_styr_protocol.h"
#include "arm.h"
#include "motor.h"

/* The following datatypes are meant to be a readable list of commands to be 
	forwarded to the specified servo */
typedef struct command_struct
{
	uint8_t instruction;
	servo_parameter_t *first_parameter;
	
	/* Comparing status with expected length of recieved message
		tells us whether we have recieved the whole message */
	uint8_t status;
	uint8_t length;
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
	arm_data_t *arm;
	motor_data_t *motor;
} command_queue_t;


/* Core functions for command_queue */
void system_init(command_queue_t *q, int motors, int servos);
void input_byte(command_queue_t *q, uint8_t data);

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
int set_node_command(command_queue_node_t *node, int data);

/* Functions for command */
int set_command(command_struct_t *command, uint8_t data);
command_struct_t* new_command();
void read_command(command_queue_t *q);
void read_all_commands(command_queue_t *q);
int command_status(command_struct_t *current);
bool command_recieved(command_struct_t *c);

#endif /* COMMAND_QUEUE_H_ */