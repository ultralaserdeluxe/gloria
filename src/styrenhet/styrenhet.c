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
#include "arm.h"

command_queue_t *gloria_queue;

void spi_recieve_handler(unsigned int data)
{
	input_byte(gloria_queue, data);
}

int main(void)
{
	arm_init(SERVO_ALL);
	gloria_queue = new_queue();
	system_init(gloria_queue, 2, 8);
	spi_slave_init();
	sei();
	
	while(1){
		input_byte(gloria_queue, 0x03); // Flytta Axel 6 til 02ff
		input_byte(gloria_queue, 0x16);
		input_byte(gloria_queue, 0x02);
		input_byte(gloria_queue, 0xff);
		
		input_byte(gloria_queue, 0x01);
		input_byte(gloria_queue, 0x36); // Action Axel ALL
		
		read_all_commands(gloria_queue);
		_delay_ms(1500);
		
		input_byte(gloria_queue, 0x03); // Flytta Axel 6 til 02ff
		input_byte(gloria_queue, 0x16);
		input_byte(gloria_queue, 0x02);
		input_byte(gloria_queue, 0x0f);
		
		input_byte(gloria_queue, 0x01);
		input_byte(gloria_queue, 0x36); // Action Axel ALL
		
		read_all_commands(gloria_queue);
		_delay_ms(1500);
		
	}
}