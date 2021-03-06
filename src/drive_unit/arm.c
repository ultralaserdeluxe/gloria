/*
 * arm.c
 *
 * Created: 2014-11-08 14:57:57
 * Description: Functions for handling our arm.
 */ 

#define F_CPU 16000000UL
#include "arm.h"
#include "usart.h"
#include "parameter_chain.h"
#include <util/delay.h>
#include <util/atomic.h>

/* Initializes our arm */
void arm_init(arm_data_t *arm)
{
	for (int i = SERVO_1; i <= SERVO_8; i++)
	{
		servo_init(i);
		arm->s[i].goal_speed_h = P_GOAL_SPEED_H_INIT;
		arm->s[i].goal_speed_l = P_GOAL_SPEED_L_INIT;
		arm->s[i].ID = i;
	}
}

void update_servo(arm_data_t *d, int address)
{
	/* Update servo goal position */
	uint8_t servo_id = d->s[address].ID;
	
	uint8_t goal_speed_h = d->s[address].goal_speed_h;
	uint8_t goal_speed_l = d->s[address].goal_speed_l;
	uint8_t goal_position_h = d->s[address].goal_position_h;
	uint8_t goal_position_l = d->s[address].goal_position_l;
	// Todo: Debug
	//uint8_t goal_speed_l = P_GOAL_SPEED_L_INIT;
	//uint8_t goal_speed_h = P_GOAL_SPEED_H_INIT;
	servo_parameter_t *p = create_servo_parameter(goal_position_l);
	add_servo_parameter_chain(p, goal_position_h);
	add_servo_parameter_chain(p, goal_speed_l);
	add_servo_parameter_chain(p, goal_speed_h);
	send_servo_instruction(
		servo_instruction_packet(servo_id, INSTR_REG_WRITE, P_GOAL_POSITION_L, p)
	);
	
	free_servo_parameter_chain(p);
}

void update_servo_regs(arm_data_t *d, int address)
{
	if (address == SERVO_ALL)
	{
		for (int i = 1; i < d->length; i++)
		{
			update_servo(d, i);
			/* Todo: Delay to ensure that the servo has time to accept instruction 
			* Should this be here? */
			_delay_us(500);
		}
	}
	else
	{
		update_servo(d, address);
	}
}

/* Called when Action detected on SPI */
void arm_action(int address)
{	
	/* Send action command */
	send_servo_instruction(
		servo_instruction_packet(address, INSTR_ACTION, 0, NULL)
	);
}

arm_data_t* new_arm_data(int number_of_servos)
{
	arm_data_t *this = malloc(sizeof(arm_data_t));
	this->length = number_of_servos;
	/* Since our servos are in the range 1-n, we get an empty servo in the beginning */
	this->s = malloc((number_of_servos + 1) * sizeof(servo_data_t));
	//for (int i = 0; i < number_of_servos; i++)
	//{
		//this->s[i].goal_speed_l = P_GOAL_SPEED_L_INIT;
		//this->s[i].goal_speed_h = P_GOAL_SPEED_H_INIT;
	//}
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
	uint16_t temp = high;
	return (temp << 8) + low;
}

void set_inverse_servo_goal_position(arm_data_t *arm, int servo, uint8_t new_position_h, uint8_t new_position_l)
{
	servo_data_t *array = arm->s;
	uint16_t goal_position = 0x3ff - make_int_16(new_position_h, new_position_l);
	array[servo].goal_position_h = (goal_position >> 8) & 0x03;
	array[servo].goal_position_l = goal_position & 0xFF;
}

void update_servo_status(arm_data_t *arm, int id)
{
	/* Tell servo id that we want to read 4 regs, present position l/h, speed l/h */
	servo_parameter_t *p = create_servo_parameter(4);
	send_servo_instruction(
		servo_instruction_packet(id, INSTR_READ, P_PRESENT_POSITION_L, p)
	);
	free_servo_parameter_chain(p);
	_delay_us(10); //Wait for last command to send properly
	usart_set_rx();
	
	_delay_ms(10); // Wait for command to be recieved
	////usart_receive(); //Todo: Why is this random byte necessary?
	/*usart_receive(); //0xff
	usart_receive(); //0xff
	usart_receive(); //id
	usart_receive(); //length
	
	int new_status = usart_receive();
	int new_position_l = usart_receive();
	int new_position_h = usart_receive();
	int new_speed_l = usart_receive();
	int new_speed_h = usart_receive();
	usart_receive(); //checksum
	*/
	
	usart_pop_recieve();
	usart_pop_recieve();
	usart_pop_recieve();
	usart_pop_recieve();
	
	int new_status = usart_pop_recieve();
	int new_position_l = usart_pop_recieve();
	int new_position_h = usart_pop_recieve();
	int new_speed_l = usart_pop_recieve();
	int new_speed_h = usart_pop_recieve();
	
	usart_pop_recieve();
	
	usart_set_tx();
	
	ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
	{
		// Todo: Possible to return NULL or -1?
		if (new_status > 0)		arm->s[id].status = new_status;
		if (new_position_l > 0)	arm->s[id].position_l = new_position_l;
		if (new_position_h > 0)	arm->s[id].position_h = new_position_h;
		if (new_speed_l > 0)	arm->s[id].speed_l = new_speed_l;
		if (new_speed_h > 0)	arm->s[id].speed_h = new_speed_h;
	}
}