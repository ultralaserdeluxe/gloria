/*
 * styrenhet.c
 *
 * Created: 2014-11-06
 * Description: Main file.
 */ 

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

void spi_recieve_handler(unsigned int data){
	
}