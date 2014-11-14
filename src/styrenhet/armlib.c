/*
 * armlib.c
 *
 * Created: 2014-11-08 17:53:04
 * Description: Functions for the arm
 */ 


#include "armlib.h"


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

arm_instruction_t* create_instructions(int amount)
{
	arm_instruction_t *this = malloc(sizeof(arm_instruction_t)*amount);
	this->length = 0;
	return this;
}

arm_instruction_t* concatenate_instructions(arm_instruction_t *t1, arm_instruction_t *t2)
{
	t1->last_parameter->next = t2->first_parameter;
	t1->last_parameter = t2->last_parameter;
	free(t2);
}

void free_instruction(arm_instruction_t *t)
{
	free(t);
}

void free_instruction_full(arm_instruction_t *t)
{
	parameter_t *current = t->first_parameter;
	while(!empty_parameter(current))
	{
		t->first_parameter = current->next;
		free(current);
		current = t->first_parameter;
	}
	free_instruction(t);
}

parameter_t* create_parameter(unsigned int new_parameter)
{
	parameter_t *this = malloc(sizeof(parameter_t));
	this->current_parameter = new_parameter;
	return this;
}

void add_parameter(arm_instruction_t *instr, unsigned int new_parameter)
{
	if (empty_parameter(instr->first_parameter))
	{
		instr->first_parameter = create_parameter(new_parameter);
	}
	else
	{
		parameter_t *last = last_parameter(instr->first_parameter);
		last->next = create_parameter(new_parameter);
	}
	instr->length++;
}

parameter_t* get_parameter(arm_instruction_t *instr)
{
	return instr->first_parameter;
}

parameter_t* next_parameter(parameter_t *p)
{
	return p->next;
}

bool empty_parameter(parameter_t *p)
{
	if (p == NULL) return true;
	else return false;
}

parameter_t* last_parameter(parameter_t *p)
{
	if (p->next == NULL) return p;
	else
	{
		parameter_t *current = p;
		while (current->next != NULL)
		{
			current = current->next;
		}
		return current;
	}
}

unsigned int parameter_value(parameter_t *p)
{
	return p->current_parameter;
}