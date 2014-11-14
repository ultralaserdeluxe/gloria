/*
 * styrenhet.c
 *
 * Created: 2014-11-06
 * Description: Main file.
 */ 

#define ARM_WRITE_DATA 0x03
#define ARM_ACTION 0x05

#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "spi.h"
#include "usart.h"
#include "styrenhet.h"

uint8_t make_checksum(uint8_t ID, uint8_t length, uint8_t instr, uint8_t para)
{
	return ~(ID + length + instr + para);
}

int main(void)
{
	/* Set baud to clk/16 => 1Mbps */
	usart_init();
	
	uint8_t id = SERVO_6;
	uint8_t length = 0x07;
	uint8_t instruction = INST_WRITE;
	
	usart_set_tx();

	uint8_t p1 = P_CW_ANGLE_LIMIT_L;
	uint8_t p2 = 0x00;
	uint8_t p3 = 0x00;
	uint8_t p4 = 0xFF;
	uint8_t p5 = 0x03;
	usart_transmit(0xFF);
	usart_transmit(0xFF);
	usart_transmit(id);
	usart_transmit(length);
	usart_transmit(instruction);
	usart_transmit(p1);
	usart_transmit(p2);
	usart_transmit(p3);
	usart_transmit(p4);
	usart_transmit(p5);
	usart_transmit(make_checksum(id, length, instruction,
								p1 + p2 + p3 + p4 + p5));
	
									
	p1 = P_CW_COMPLIANCE_MARGIN;
	p2 = 0x00;
	p3 = 0x00;
	p4 = 0x20;
	p5 = 0x20;
	usart_transmit(0xFF);
	usart_transmit(0xFF);
	usart_transmit(id);
	usart_transmit(length);
	usart_transmit(instruction);
	usart_transmit(p1);
	usart_transmit(p2);
	usart_transmit(p3);
	usart_transmit(p4);
	usart_transmit(p5);
	usart_transmit(make_checksum(id, length, instruction,
								p1 + p2 + p3 + p4 + p5));
								
	length = 0x04;
	p1 = P_TORQUE_ENABLE;
	p2 = OFF;
	usart_transmit(0xFF);
	usart_transmit(0xFF);
	usart_transmit(id);
	usart_transmit(length);
	usart_transmit(instruction);
	usart_transmit(p1);
	usart_transmit(p2);
	usart_transmit(make_checksum(id, length, instruction,
								p1 + p2));

	length = 0x05;
	p1 = P_GOAL_SPEED_L;
	p2 = 0xFF;
	p3 = 0x03;
	usart_transmit(0xFF);
	usart_transmit(0xFF);
	usart_transmit(id);
	usart_transmit(length);
	usart_transmit(instruction);
	usart_transmit(p1);
	usart_transmit(p2);
	usart_transmit(p3);
	usart_transmit(make_checksum(id, length, instruction,
								p1 + p2 + p3));	
	
	length = 0x05;
	p1 = P_GOAL_POSITION_L;
	p2 = 0xff;
	p3 = 0x02;	
	while(1){
	
		usart_transmit(0xFF);
		usart_transmit(0xFF);
		usart_transmit(id);
		usart_transmit(length);
		usart_transmit(instruction);
		usart_transmit(p1);
		usart_transmit(p2);
		usart_transmit(p3);
		usart_transmit(make_checksum(id, length, instruction,
									p1 + p2 + p3));
								
		/*_delay_ms(3000);*/
	
		p3 = p3 ^ 0x02;
	}
}


void do_action(int address, queue_t *q)
{
	queue_node_t *current = q->head;
	while(current->next != NULL)
	{
		switch(address)
		{
		case 0x00:
			//Do if motor right
		case 0x01:
			//Do if motor left
		case 0x02:
			//Do if arm axel 1
		default:
			break;
		}
	}
}

/* Set register reg on arm ID to new_value */
arm_instruction_t* set_arm(int ID, int reg, int new_value)
{
	arm_instruction_t *t = create_instructions(1);
	add_parameter(t,0xFF);
	add_parameter(t,0xFF);
	add_parameter(t,ID);
	add_parameter(t,0x04); //Length
	add_parameter(t,reg);
	add_parameter(t,new_value);
	add_parameter(t,make_checksum(ID, 0x04, reg, new_value));
	return t;
}

/* Send an Action instruction to arm with id ID */
arm_instruction_t* arm_action(int ID)
{
	arm_instruction_t *t = create_instructions(1);
	add_parameter(t,0xFF);
	add_parameter(t,0xFF);
	add_parameter(t,ID);
	add_parameter(t,0x02); //Length
	add_parameter(t,0x05)
	add_parameter(t,make_checksum(ID, 0x02, 0x05, 0));
	return t;
}

/* Convert command from DAD into instruction to arm */
/* URGENT: Need to be able to make 2 instructions from a command! */
arm_instruction_t* command_to_arm_instr(command_struct_t *c)
{
	int instr;
	/* Interpret instruction */
	switch(c->instruction & 0xF0)
	{
		case 1:
			instr = ARM_WRITE_DATA;	//Set register
			break;
		case 2:
			instr = ARM_ACTION;	//Do Action
			break;
	}
	/* Make instructions for the adressed servos */
	switch (c->instruction & 0x0F)
	{
	case 0xF0:
	case 0xD0:
		if (instr == ARM_WRITE_DATA)
		{
			return set_arm(0xFE,c->data_1,c->data_2);
		}
		else if (instr == ARM_ACTION)
		{
			return arm_action(0xFE);
		}
		break;
	case 0x02:
		// Axel 1
		break;
	case 0x04:
		// Axel 2
		break;
	case 0x06:
		// Axel 3
		break;
	case 0x08:
		// Axel 4
		break;
	case 0x0B:
		// Axel 5
		break;
	}