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
#include "command_queue.h"
#include "spi.h"
#include "ax12a.h"
#include "huvud_styr_protocol.h"
#include "usart.h" //USART communication handled by servo.c

command_queue_t *gloria_queue;

void spi_recieve_handler(unsigned int data)
{
	
}

int main(void)
{
	arm_init(SERVO_ALL);
	gloria_queue = new_queue();

	int id = SERVO_6;
	int instruction = INSTR_WRITE;
	uint8_t length = 0x05;
	uint8_t p1 = P_GOAL_SPEED_L;
	uint8_t p2 = 0xFF;
	uint8_t p3 = 0x03;
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