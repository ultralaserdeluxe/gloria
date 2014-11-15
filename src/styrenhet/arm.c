/*
 * arm.c
 *
 * Created: 2014-11-08 14:57:57
 * Description: Functions for handling our arm.
 */ 

#include "arm.h"

/* Initializes our arm, its servos and returns a new command_queue */
void arm_init(int servo)
{
	servo_init(servo);
}

void update_servo_regs(int address, arm_data_t *d)
{
		/* Update servo goal position */
		servo_parameter_t *p = NULL;
		uint8_t goal_position_h = d->s[address].goal_position_h;
		uint8_t goal_position_l = d->s[address].goal_position_l;
		add_servo_parameter_chain(p, goal_position_l);
		add_servo_parameter_chain(p, goal_position_h);
		send_servo_instruction(
		servo_instruction_packet(address, INSTR_REG_WRITE, P_GOAL_POSITION_L, p)
		);

		/* Update servo goal speed */
		free_servo_parameter_chain(p);
		uint8_t goal_speed_h = d->s[address].goal_speed_h;
		uint8_t goal_speed_l = d->s[address].goal_speed_l;
		add_servo_parameter_chain(p, goal_speed_l);
		add_servo_parameter_chain(p, goal_speed_h);
		send_servo_instruction(
		servo_instruction_packet(address, INSTR_REG_WRITE, P_GOAL_SPEED_L, p)
		);
}

/* Called when Action detected on SPI */
void arm_action(int address)
{	
	/* Send action command */
	send_servo_instruction(
		servo_instruction_packet(address, INSTR_ACTION, 0, 0)
	);
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

void set_servo_speed(arm_data_t *arm, int servo, uint8_t new_speed_h, uint8_t new_speed_l)
{
	servo_data_t *array = arm->s;
	array[servo].speed_h = new_speed_h;
	array[servo].speed_l = new_speed_l;
}

void set_servo_position(arm_data_t *arm, int servo, uint8_t new_position_h, uint8_t new_position_l)
{
	servo_data_t *array = arm->s;
	array[servo].position_h = new_position_h;
	array[servo].position_l = new_position_l;
}

uint16_t get_servo_speed(arm_data_t *arm, int servo)
{
	servo_data_t *array = arm->s;
	return make_int_16(array[servo].speed_h, array[servo].speed_l);
}

uint16_t get_servo_position(arm_data_t *arm, int servo)
{
	servo_data_t *array = arm->s;
	return make_int_16(array[servo].position_h, array[servo].position_l);
}

void set_servo_goal_speed(arm_data_t *arm, int servo, uint8_t new_speed_h, uint8_t new_speed_l)
{
	servo_data_t *array = arm->s;
	array[servo].goal_speed_h = new_speed_h;
	array[servo].goal_speed_l = new_speed_l;
}

void set_servo_goal_position(arm_data_t *arm, int servo, uint8_t new_position_h, uint8_t new_position_l)
{
	servo_data_t *array = arm->s;
	array[servo].goal_position_h = new_position_h;
	array[servo].goal_position_l = new_position_l;
}

uint16_t get_servo_goal_speed(arm_data_t *arm, int servo)
{
	servo_data_t *array = arm->s;
	return make_int_16(array[servo].goal_speed_h, array[servo].goal_speed_l);
}

uint16_t get_servo_goal_position(arm_data_t *arm, int servo)
{
	servo_data_t *array = arm->s;
	return make_int_16(array[servo].goal_position_h, array[servo].goal_position_l);
}

uint16_t make_int_16(uint8_t high, uint8_t low)
{
	return (high << 4) + low;
}