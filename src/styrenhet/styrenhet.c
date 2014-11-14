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
#include "command_queue.h"
#include "armlib.h"

/* Global queue of received commands */
queue_t *queue_arm;
queue_t *queue_motors;

uint8_t make_checksum(uint8_t ID, uint8_t length, uint8_t instr, uint8_t para)
{
	return ~(ID + length + instr + para);
}

int main(void)
{
	//my_queue = new_queue();
	
	/* port a = output */
	//DDRA = 0xFF;
	DDRC = 0xFF; //PORTC as output
	DDRB = 0xFF;
		
	/* Init SPI and enable global interrupts */
	//spi_slave_init();
	//sei();
	
	DDRD = 0xFF;
	TCCR2A = (1<<COM2A1)|(1<<COM2B1)|(1<<WGM20);
	TCCR2B = (0<<WGM22)|(0<<CS21)|(1<<CS20);
	
	OCR2A = OCR2B = 0x00;
	
	PORTA = 0x81; // set dir
		
	/* Set baud to clk/16 => 1Mbps */
	usart_init();
	//uint8_t ID = 0x01;
	//uint8_t length = 0x02;
	//uint8_t instr = 0x01;
	//uint8_t para = 0x00;
	//uint8_t test;
	//PORTC = usart_receive();

	uint8_t speed;
	PORTB = 0x01;
	
	while(1) 
	{
		speed++;
		usart_transmit(speed);
		_delay_ms(100);
		
		/*
		for(speed = 0; speed < 250; speed++){
			OCR2A = OCR2B = speed;
			_delay_ms(10);
		}
		for(; speed > 0; speed--){
			OCR2A = OCR2B = speed;
			_delay_ms(10);
		}
		*/
		
	};
}

void spi_recieve_handler(unsigned int data)
{
	/* Take data, put in current command. Create new if current is done.
		Perform actions if action command */
	PORTA = data;
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
}