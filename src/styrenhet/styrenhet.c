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
	gloria_queue = new_queue();
	system_init(gloria_queue, 2, 8);
	arm_init(gloria_queue->arm);
	//servo_init(SERVO_1);
	//servo_init(SERVO_2);
	//servo_init(SERVO_3);
	//servo_init(SERVO_4);
	//servo_init(SERVO_5);
	//servo_init(SERVO_6);
	//servo_init(SERVO_7);
	//servo_init(SERVO_8);
	spi_slave_init();
	sei();
	
	//int id = SERVO_1;
	////arm_init(gloria_queue->arm);
	//servo_init(id);
	//set_servo_goal_speed(gloria_queue->arm, id, 0x00, 0xff);

	while(1){
		
		read_all_commands(gloria_queue);
		//motor_action(MOTOR_ALL, gloria_queue->motor);

		/* Debug 1 - Simulate input from SPI */
		
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x16);
		//input_byte(gloria_queue, 0x00);
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
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x1D);
		//input_byte(gloria_queue, 0x00);
		//input_byte(gloria_queue, 0xff);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x3F); // Action
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x16);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0xff);
		//
		//read_all_commands(gloria_queue);
		//_delay_ms(2500);
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
		//input_byte(gloria_queue, 0x03); // Flytta Axel
		//input_byte(gloria_queue, 0x1D);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0xff);
		//
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0xff);
		//input_byte(gloria_queue, 0x01);
		//input_byte(gloria_queue, 0x3F); // Action
		//
		//read_all_commands(gloria_queue);
		//_delay_ms(2500);
		
		
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