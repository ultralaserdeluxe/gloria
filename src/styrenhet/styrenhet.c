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

void activate_send(void)
{
  PORTB |= (1<<PORTB0);
  PORTB |= 
    (1<<PORTB0)|
    (0<<PORTB1)|
    (1<<PORTB2)|
    (1<<PORTB3)|
    (1<<PORTB4)|
    (1<<PORTB5)|
    (1<<PORTB6)|
    (1<<PORTB7)|
}

void activate_receive(void)
{
  PORTB |= (1<<PORTB1);
  PORTB |= 
    (0<<PORTB0)|
    (1<<PORTB1)|
    (1<<PORTB2)|
    (1<<PORTB3)|
    (1<<PORTB4)|
    (1<<PORTB5)|
    (1<<PORTB6)|
    (1<<PORTB7)|
}

int main(void)
{
	//my_queue = new_queue();
	
	/* port a = output */
	//DDRA = 0xFF;
	DDRC = 0xFF; //PORTC as output
	
	DDRA = 0xFF; //FOR DEBUGGING
	
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
	uint8_t ID = SERVO_1;
	uint8_t length = 0x02;
	uint8_t instr = INST_PING;
	uint8_t param1 = P_LED;
	
	
	while(1) 
	{
	  _delay_ms(1);
	  activate_send();
	  _delay_ms(1);
	  usart_transmit(0xFF);
	  usart_transmit(0xFF);
	  usart_transmit(ID);
	  usart_transmit(length);
	  usart_transmit(instr);
	  usart_transmit(make_checksum(ID, length, instr, 0));


	  _delay_ms(1);
	  activate_receive();
	  PORTA = usart_receive();
	  PORTA = usart_receive();
	  PORTA = usart_receive();
	  PORTA = usart_receive();
	  PORTA = usart_receive();
	  PORTA = usart_receive();
	  	  
	  
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
