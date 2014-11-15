/*
 * arm.c
 *
 * Created: 2014-11-08 14:57:57
 * Description: Functions for handling our arm.
 */ 

#include "arm.h"

/* Initializes our arm, its servos and returns a new command_queue */
command_queue_t* arm_init(int servo)
{
	servo_init(servo);
	return new_queue();
}

/* Convert command into instruction to arm */
/* URGENT: Need to be able to make 2 instructions from a command! */
servo_instruction_t* command_to_arm_instr(command_struct_t *c)
{
	
}

/* Called when Action detected on SPI */
void do_action(int address, command_queue_t *q)
{
	
}

/* Create a new queue, with one empty entry */
command_queue_t* new_queue()
{
	command_queue_t *this = malloc(sizeof(command_queue_t));
	this->head = NULL;
	this->last = NULL;
	return this;
}

void free_queue(command_queue_t *q)
{
	command_queue_node_t *current;
	while(q->head != NULL)
	{
		current = q->head;
		q->head = current->next;
		free_node(current);
	}
	free(q);
}

/* Add new node to end of queue */
void put_queue(command_queue_t *q, command_queue_node_t *node)
{
	if (empty_queue(q))
	{
		q->head = node;
		q->last = node;
	}
	else
	{
		q->last->next = node;
		q->last = node;
	}
}

/* Remove and return first entry */
command_queue_node_t* pop_first(command_queue_t *q)
{
	command_queue_node_t *node = q->head;
	q->head = node->next;
	return node;
}

/* Remove node *node from queue */
void remove_node(command_queue_t *q, command_queue_node_t *node)
{
	if (empty_queue(q))
	{
		return;
	}
	
	command_queue_node_t *current = q->head;
	if (node == first_node(q))
	{
		q->head = node->next;
		current = q->head;
	}
	else
	{
		while (current->next != node)
		{
			if (current->next == NULL)
			{
				/* Node not in queue */
				return;
			}
			current = current->next;
		}
		current->next = node->next;
	}
	
	if (node == last_node(q))
	{
		q->last = current;
	}
}

bool empty_queue(command_queue_t *this)
{
	if (this->head == NULL)
	{
		return true;
	}
	else
	{
		return false;
	}
}

command_queue_node_t* first_node(command_queue_t *this)
{
	return this->head;
}

command_queue_node_t* last_node(command_queue_t *this)
{
	return this->last;
}

command_queue_node_t* next_node(command_queue_node_t *node)
{
	return node->next;
}

/* Returns a new node */
command_queue_node_t* new_node()
{
	command_queue_node_t *this;
	this = malloc(sizeof(command_queue_node_t));
	this->command = new_command();
	return this;
}

/* Frees node and returns pointer to next node */
command_queue_node_t* free_node(command_queue_node_t* this)
{
	command_queue_node_t *next_node = this->next;
	free_servo_parameter_chain(this->command->first_parameter);
	free(this->command);
	free(this);
	return next_node;
}

command_struct_t* node_data(command_queue_node_t *node)
{
	return node->command;
}

/* Abstraction wrapper for set_command */
int set_node_command(command_queue_node_t *node, int chooser, int data)
{
	return set_command(node->command, chooser, data);
}

/* Sets a part of command command, chosen with chooser to data. 
	Returns updated status */
int set_command(command_struct_t *command, int chooser, uint8_t data)
{
	switch (chooser)
	{
		case 0 :
			command->instruction = data;
			command->status++;
			return command->status;
		default :
			add_servo_parameter_chain(command->first_parameter, data);
			command->status++;
			return command->status;
	}
}

/* Returns a new command struct with status = 0, others null */
command_struct_t* new_command()
{
	command_struct_t *this;
	this = malloc(sizeof(command_struct_t));
	this->status = 0;
	return this;
}

/* Returns current status */
int command_status(command_struct_t current)
{
	return current.status;
}

arm_data_t* new_arm_data(int number_of_servos)
{
	arm_data_t *this = malloc(sizeof(arm_data_t));
	this->length = number_of_servos;
	this->s = malloc(number_of_servos * sizeof(servo_data_t));
	return this;
}

void free_arm_data(arm_data_t *arm)
{
	free(arm->s);
	free(arm);
}

void set_servo_speed(arm_data_t *arm, int servo, unsigned int new_speed)
{
	servo_data_t *array = arm->s;
	array[servo].speed = new_speed;
}

void set_servo_position(arm_data_t *arm, int servo, unsigned int new_position)
{
	servo_data_t *array = arm->s;
	array[servo].position = new_position;
}

int get_servo_speed(arm_data_t *arm, int servo)
{
	servo_data_t *array = arm->s;
	return array[servo].speed;
}

int get_servo_position(arm_data_t *arm, int servo)
{
	servo_data_t *array = arm->s;
	return array[servo].position;
}

void set_servo_goal_speed(arm_data_t *arm, int servo, unsigned int new_speed)
{
	servo_data_t *array = arm->s;
	array[servo].goal_speed = new_speed;
}

void set_servo_goal_position(arm_data_t *arm, int servo, unsigned int new_position)
{
	servo_data_t *array = arm->s;
	array[servo].goal_position = new_position;
}

int get_servo_goal_speed(arm_data_t *arm, int servo)
{
	servo_data_t *array = arm->s;
	return array[servo].goal_speed;
}

int get_servo_goal_position(arm_data_t *arm, int servo)
{
	servo_data_t *array = arm->s;
	return array[servo].goal_position;
}