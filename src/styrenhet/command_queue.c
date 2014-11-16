/*
 * command_queue.c
 *
 * Created: 2014-11-15 16:28:17
 *  Author: Hannes
 *	Description: lol-commands
 */ 

#include "command_queue.h"

/* Initialize arm and motor */
void system_init(command_queue_t *q, int motors, int servos)
{
	q->arm = new_arm_data(servos + 1); //We have one "extra" servo. SERVO_0 (doesnt exist)
	for (int i = 0; i <= SERVO_8; i++)
	{
		q->arm->s[i].ID = i;
	}
	q->motor = new_motor_data(motors);
	for (int i = MOTOR_LEFT; i <= MOTOR_RIGHT; i++)
	{
		q->motor->s[i].ID = i;
	}
}

void input_byte(command_queue_t *q, uint8_t data)
{
	// To do, take input byte, decide if data is corrupt or not
	if (empty_queue(q))
	{
		put_queue(q, new_node());
		int status = set_node_command(last_node(q), data);
	}
	else if (!command_recieved(node_data(last_node(q))))
	{
		set_node_command(last_node(q), data);
	}
	else
	{
		put_queue(q, new_node());
		int status = set_node_command(last_node(q), data);
	}
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
int set_node_command(command_queue_node_t *node, int data)
{
	return set_command(node->command, data);
}

/* Sets a part of command command, chosen with chooser to data. 
	Returns updated status */
int set_command(command_struct_t *command, uint8_t data)
{
	switch (command->status)
	{
		case 0 :
			command->length = data;
			command->status++;
			break;
		case 1 :
			command->instruction = data;
			command->status++;
			break;
		case 2:
			command->first_parameter = create_servo_parameter(data);
			command->status++;
			break;
		default :
			add_servo_parameter_chain(command->first_parameter, data);
			command->status++;
			break;
	}
	return command->status;
}

/* Returns a new command struct with status = 0, others null */
command_struct_t* new_command()
{
	command_struct_t *this;
	this = malloc(sizeof(command_struct_t));
	this->status = 0;
	this->length = 0;
	return this;
}

void read_command(command_queue_t *q)
{
	if (!command_recieved(node_data(first_node(q))))
	{
		return;
	}
	command_queue_node_t *n = pop_first(q);
	command_struct_t *c = node_data(n);
	/* If we have Action, perform action */
	if ((c->instruction & COMMAND_INSTRUCTION_MASK) == COMMAND_ACTION)
	{
		switch (c->instruction & COMMAND_ADDRESS_MASK)
		{
		case ADDRESS_ALL:
			arm_action(SERVO_ALL);
			motor_action(MOTOR_ALL, q->motor);
			break;
		case ADDRESS_ARM:
			arm_action(SERVO_ALL);
			break;
		case ADDRESS_JOINT_1:
			arm_action(SERVO_1);
			break;
		case ADDRESS_JOINT_2:
			arm_action(SERVO_2);
			arm_action(SERVO_3);
			break;
		case ADDRESS_JOINT_3:
			arm_action(SERVO_4);
			arm_action(SERVO_5);
			break;
		case ADDRESS_JOINT_4:
			arm_action(SERVO_6);
			break;
		case ADDRESS_JOINT_5:
			arm_action(SERVO_7);
			break;
		case ADDRESS_JOINT_6:
			arm_action(SERVO_8);
			break;
		case ADDRESS_MOTOR_ALL:
			motor_action(MOTOR_ALL, q->motor);
			break;
		case ADDRESS_MOTOR_L:
			motor_action(MOTOR_LEFT, q->motor);
			break;
		case ADDRESS_MOTOR_R:
			motor_action(MOTOR_RIGHT, q->motor);
			break;
		}
	}
	else if ((c->instruction & COMMAND_INSTRUCTION_MASK) == COMMAND_SET_REG)
	{
		servo_parameter_t *p = c->first_parameter;
		switch (c->instruction & COMMAND_ADDRESS_MASK)
		{
		case ADDRESS_ARM:
			set_servo_goal_position(q->arm, SERVO_1, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_position(q->arm, SERVO_2, p->current_parameter, next_servo_parameter(p)->current_parameter);
			/* SERVO_3 is same joint as SERVO_2 and has to be its inverse */
			set_servo_goal_position(q->arm, SERVO_3, ~(p->current_parameter), ~(next_servo_parameter(p)->current_parameter));
			set_servo_goal_position(q->arm, SERVO_4, p->current_parameter, next_servo_parameter(p)->current_parameter);
			/* SERVO_5 is same joint as SERVO_4 and has to be its inverse */
			set_servo_goal_position(q->arm, SERVO_5, ~(p->current_parameter), ~(next_servo_parameter(p)->current_parameter));
			set_servo_goal_position(q->arm, SERVO_6, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_position(q->arm, SERVO_7, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_position(q->arm, SERVO_8, p->current_parameter, next_servo_parameter(p)->current_parameter);
			update_servo_regs(q->arm, SERVO_ALL);
			break;
		case ADDRESS_JOINT_1:
			set_servo_goal_position(q->arm, SERVO_1, p->current_parameter, next_servo_parameter(p)->current_parameter);
			update_servo_regs(q->arm, SERVO_1);
			break;
		case ADDRESS_JOINT_2:
			set_servo_goal_position(q->arm, SERVO_2, p->current_parameter, next_servo_parameter(p)->current_parameter);
			/* SERVO_3 is same joint as SERVO_2 and has to be its inverse */
			set_servo_goal_position(q->arm, SERVO_3, ~(p->current_parameter), ~(next_servo_parameter(p)->current_parameter));
			update_servo_regs(q->arm, SERVO_2);
			update_servo_regs(q->arm, SERVO_3);
			break;
		case ADDRESS_JOINT_3:
			set_servo_goal_position(q->arm, SERVO_4, p->current_parameter, next_servo_parameter(p)->current_parameter);
			/* SERVO_5 is same joint as SERVO_4 and has to be its inverse */
			set_servo_goal_position(q->arm, SERVO_5, ~(p->current_parameter), ~(next_servo_parameter(p)->current_parameter));
			update_servo_regs(q->arm, SERVO_4);
			update_servo_regs(q->arm, SERVO_5);
			break;
		case ADDRESS_JOINT_4:
			set_servo_goal_position(q->arm, SERVO_6, p->current_parameter, next_servo_parameter(p)->current_parameter);
			update_servo_regs(q->arm, SERVO_6);
			break;
		case ADDRESS_JOINT_5:
			set_servo_goal_position(q->arm, SERVO_7, p->current_parameter, next_servo_parameter(p)->current_parameter);
			update_servo_regs(q->arm, SERVO_7);
			break;
		case ADDRESS_JOINT_6:
			set_servo_goal_position(q->arm, SERVO_8, p->current_parameter, next_servo_parameter(p)->current_parameter);
			update_servo_regs(q->arm, SERVO_7);
			break;
		case ADDRESS_MOTOR_ALL:
			set_queued_speed_left(q->motor, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_queued_speed_right(q->motor, p->current_parameter, next_servo_parameter(p)->current_parameter);
			break;
		case ADDRESS_MOTOR_L:
			set_queued_speed_left(q->motor, p->current_parameter, next_servo_parameter(p)->current_parameter);
			break;
		case ADDRESS_MOTOR_R:
			set_queued_speed_left(q->motor, p->current_parameter, next_servo_parameter(p)->current_parameter);
			break;
		}
	}
	else if ((c->instruction & COMMAND_INSTRUCTION_MASK) == COMMAND_SET_JOINT_SPEED)
	{
		servo_parameter_t *p = c->first_parameter;
		switch (c->instruction & COMMAND_ADDRESS_MASK)
		{
		case ADDRESS_ARM:
			set_servo_goal_speed(q->arm, SERVO_1, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_speed(q->arm, SERVO_2, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_speed(q->arm, SERVO_3, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_speed(q->arm, SERVO_4, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_speed(q->arm, SERVO_5, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_speed(q->arm, SERVO_6, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_speed(q->arm, SERVO_7, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_speed(q->arm, SERVO_8, p->current_parameter, next_servo_parameter(p)->current_parameter);
			break;
		case ADDRESS_JOINT_1:
			set_servo_goal_speed(q->arm, SERVO_1, p->current_parameter, next_servo_parameter(p)->current_parameter);
			break;
		case ADDRESS_JOINT_2:
			set_servo_goal_speed(q->arm, SERVO_2, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_speed(q->arm, SERVO_3, p->current_parameter, next_servo_parameter(p)->current_parameter);
			break;
		case ADDRESS_JOINT_3:
			set_servo_goal_speed(q->arm, SERVO_4, p->current_parameter, next_servo_parameter(p)->current_parameter);
			set_servo_goal_speed(q->arm, SERVO_5, p->current_parameter, next_servo_parameter(p)->current_parameter);
			break;
		case ADDRESS_JOINT_4:
			set_servo_goal_speed(q->arm, SERVO_6, p->current_parameter, next_servo_parameter(p)->current_parameter);
			break;
		case ADDRESS_JOINT_5:
			set_servo_goal_speed(q->arm, SERVO_7, p->current_parameter, next_servo_parameter(p)->current_parameter);
			break;
		case ADDRESS_JOINT_6:
			set_servo_goal_speed(q->arm, SERVO_8, p->current_parameter, next_servo_parameter(p)->current_parameter);
			break;
		}
	}
	//Todo add functionality for COMMAND_STATUS
}

void read_all_commands(command_queue_t *q)
{
	while (!empty_queue(q)&&command_recieved(node_data(first_node(q))))
	{
		read_command(q);
	}
}

/* Returns current status */
int command_status(command_struct_t *current)
{
	return current->status;
}

/* Returns true if command has recieved expected amount of parameters */
bool command_recieved(command_struct_t *c)
{
	if (c->status >= c->length + COMMAND_STATUS_LENGTH_OFFSET) return true;
	else return false;
}