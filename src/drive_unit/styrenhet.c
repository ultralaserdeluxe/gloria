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
//#include "usart.h" //Todo: USART communication should be handled by servo.c
#include "arm.h"
#include "styrenhet.h"

void spi_recieve_handler(unsigned int data)
{
	input_byte(gloria_queue, data);
}

int main(void)
{
	gloria_queue = new_queue();
	system_init(gloria_queue, 2, 8);
	spi_slave_init();
	sei();

	//DDRA = 0xff;

	while(1){

		//usart_set_rx();
		//_delay_us(20);
		//usart_set_tx();
		//_delay_us(20);

		//for (int i = SERVO_1; i <= SERVO_8; i++)
		//{
			read_all_commands(gloria_queue);
			//update_servo_status(gloria_queue->arm, i);
			//}

		/* Servo read debug */
		//usart_set_tx();
		//update_status(gloria_queue->arm, SERVO_7);
		//PORTA = gloria_queue->arm->s[SERVO_7].speed_l;
		//usart_set_tx();

		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x12);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0xff);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x13);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0xff);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x14);
		//input_byte(gloria_queue, 0x02);
		//input_byte(gloria_queue, 0xff);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x15);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0xff);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x16);
		//input_byte(gloria_queue, 0x03);
		//input_byte(gloria_queue, 0xff);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x17);
		//input_byte(gloria_queue, 0x00);
		//input_byte(gloria_queue, 0x00);
		//

		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03);
		//input_byte(gloria_queue, 0x10);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x30);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x3F); // Action
		//
		//read_all_commands(gloria_queue);
		//_delay_ms(5000);
		//
		//update_status(gloria_queue->arm, SERVO_7);
		//PORTA = gloria_queue->arm->s[SERVO_7].speed_l;
		//usart_set_tx();

		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x12);
		//input_byte(gloria_queue, 0x00);
		//input_byte(gloria_queue, 0xff);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x13);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x30);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x14);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0xff);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x15);
		//input_byte(gloria_queue, 0x03);
		//input_byte(gloria_queue, 0x00);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x16);
		//input_byte(gloria_queue, 0x00);
		//input_byte(gloria_queue, 0x50);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x17);
		//input_byte(gloria_queue, 0x00);
		//input_byte(gloria_queue, 0xff);
		//

		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x3F); // Action
		//
		//read_all_commands(gloria_queue);
		//_delay_ms(5000);

		/* Debug 2 - Do what read_command does */
		//set_inverse_servo_goal_position(gloria_queue->arm, id, 0x00, 0x50);
		//update_servo_regs(gloria_queue->arm, id);
		//arm_action(id);
		//_delay_ms(1000);
		//
		//set_servo_goal_position(gloria_queue->arm, id, 0x00, 0x50);
		//update_servo_regs(gloria_queue->arm, id);
		//arm_action(id);
		//_delay_ms(1000);
	}
}
