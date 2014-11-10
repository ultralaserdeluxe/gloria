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
#include "command_queue.h"
#include "armlib.h"

/* Global queue of received commands */
queue_t *my_queue;

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
		
	/* Init SPI and enable global interrupts */
	spi_slave_init();
	sei();
	
	DDRD = 0xFF;
	TCCR2A = (1<<COM2A1)|(1<<COM2B1)|(1<<WGM20);
	TCCR2B = (0<<WGM22)|(0<<CS21)|(1<<CS20);
	
	OCR2A = OCR2B = 0x00;
	
	PORTA = 0x81; // set dir
		
	/* Set baud to clk/16 => 1Mbps */
	usart_init();
	uint8_t ID = 0x01;
	uint8_t length = 0x02;
	uint8_t instr = 0x01;
	uint8_t para = 0x00;
	//uint8_t test;
	PORTC = usart_receive();

	uint8_t speed;
	
	while(1) 
	{
		for(speed = 0; speed < 250; speed++){
			OCR2A = OCR2B = speed;
			_delay_ms(10);
		}
		for(; speed > 0; speed--){
			OCR2A = OCR2B = speed;
			_delay_ms(10);
		}
		{
			for (uint8_t i = 0; i < 50; i++)
			{
				/* read memoryplace i from servo ID 
					Put on PORTC for debug */
				_delay_ms(100);
				usart_transmit(0xFF);
				_delay_ms(1);
				usart_transmit(0xFF);
				_delay_ms(1);
				usart_transmit(ID); //ID
				_delay_ms(1);
				usart_transmit(length); //Length
				_delay_ms(1);
				usart_transmit(instr); //INstruction
				_delay_ms(1);
				//usart_transmit(i); //Address
				//_delay_ms(1);
				//usart_transmit(0x01); //Length
				//_delay_ms(1);
				usart_transmit(make_checksum(ID, length, instr, 0));	//checksum
				
			/*	PORTC = usart_receive();
				PORTC = usart_receive();
				PORTC = usart_receive();
				PORTC = usart_receive();
				PORTC = usart_receive();
				PORTC = usart_receive();
				PORTC = usart_receive();
				PORTC = usart_receive(); */
				
			}
	};
}

void spi_recieve_handler(unsigned int data)
{
	/* Take data, put in current command. Create new if current is done.
		Perform actions if action command */
	PORTA = data;
}

arm_instruction_t* recieve_arm_status()
{
	while(1)
	{
		
	}
}
