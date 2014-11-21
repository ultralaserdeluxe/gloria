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
#include "styrenhet.h"

void spi_recieve_handler(unsigned int data)
{
	input_byte(gloria_queue, data);
}

int main(void)
{
	//arm_init(SERVO_8);
	//arm_init(SERVO_7);
	//arm_init(SERVO_6);
	//arm_init(SERVO_5);
	//arm_init(SERVO_4);
	//arm_init(SERVO_3);
	//arm_init(SERVO_2);
	//arm_init(SERVO_1);
	gloria_queue = new_queue();
	system_init(gloria_queue, 2, 8);
	spi_slave_init();
	sei();
	
	while(1){
		read_all_commands(gloria_queue);
		//input_byte(gloria_queue, 0x03); // Flytta Axel 6 til 02ff
		//input_byte(gloria_queue, 0x1D);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x55);
		//
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x3D); // Action Axel ALL
		//
		//read_all_commands(gloria_queue);
		//_delay_ms(3000);
		//
		//input_byte(gloria_queue, 0x03); // Flytta Axel 6 til 02ff
		//input_byte(gloria_queue, 0x1D);
		//input_byte(gloria_queue, 0x00);
		//input_byte(gloria_queue, 0x55);
		//
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x3D); // Action Axel ALL
		//
		//read_all_commands(gloria_queue);
		//_delay_ms(3000);
		
		//input_byte(gloria_queue, 0x03); // Flytta Axel 6 til 02ff
		//input_byte(gloria_queue, 0x15);
		//input_byte(gloria_queue, 0x02);
		//input_byte(gloria_queue, 0xff);
		
		//input_byte(gloria_queue, 0x03); // Flytta Axel 5 til 02ff
		//input_byte(gloria_queue, 0x15);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0xff);
		//
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x3E); // Action Axel ALL
		//
		//read_all_commands(gloria_queue);
		//_delay_us(10);
		//usart_set_rx();
		//_delay_ms(1500);
		//usart_set_tx();
		
		//input_byte(gloria_queue, 0x03); // Flytta Axel 6 til 02ff
		//input_byte(gloria_queue, 0x15);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x00);
		
		//input_byte(gloria_queue, 0x03); // Flytta Axel 5 til 02ff
		//input_byte(gloria_queue, 0x15);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x0f);
		//
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x3E); // Action Axel ALL
		//
		//read_all_commands(gloria_queue);
		//_delay_us(10);
		//usart_set_rx();
		//_delay_ms(1500);
		//usart_set_tx();
		
	}
}