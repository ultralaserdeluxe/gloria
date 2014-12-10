/*
* usart.c
*
* Created: 2014-11-09
* Description: Functions for working with USART.
*/

#include <avr/io.h>
#include <util/atomic.h>
#include "usart.h"

void usart_init( void )
{
	/* Set tx as output. */
	DDRD |= (1<<PORTD3);
	/* Set rx as input */
	DDRD &= 0xFB;

	/*disconnect rx/tx ports*/
	DDRB |= 0x03;
	PORTB |= 0x03;

	/* Set baudrate */
	UBRR1H = 0x00;
	UBRR1L = 0x00;
	/* Enable receiver and transmitter */
	/* Enable interrupt on recieve */
	UCSR1B = (1<<RXCIE1)|(1<<RXEN1)|(1<<TXEN1);
	/* Set frame format: 8data, 2stop bit */
	UCSR1C = (3<<UCSZ10);

	/* Timer0 is used for timeout for usart_recieve */
	TCCR0A	= 0x00; /* OC0A/B as normal */
	/* Prescaler clk/1024.
	* We use the overflow flag, which gives us about 1/61Hz = 16ms */
	TCCR0B	= (1<<CS02)|(1<<CS00);
}

ISR(USART1_RX_vect)
{
	usart_put_recieve(UDR1);
}

void usart_transmit( unsigned char data )
{
	ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
	{
		TCNT0 = 0x00;
		TIFR0 |= (1<<TOV0);
		int timeout = 0;
		/* Wait for empty transmit buffer */
		while ( !( UCSR1A & (1<<UDRE1)) )
			{
				/* If time out, return NULL */
				if (TIFR0 & (1<<TOV0))
					{
						if (timeout > 3)
							{
								return;
							}
							timeout++;
							TIFR0 |= (1<<TOV0);
						}
					}
					/* Put data into buffer, sends the data */
					UDR1 = data;
				}
			}

			unsigned char usart_receive( void )
			{
				/* Reset counter and counter-flag */
				TCNT0 = 0x00;
				TIFR0 |= (1<<TOV0);
				int timeout = 0;
				/* Wait for data to be received */
				while ( !(UCSR1A & (1<<RXC1)) )
					{
						/* If time out, return NULL */
						if (TIFR0 & (1<<TOV0))
							{
								if (timeout > 3)
									{
										return 0;
									}
									timeout++;
									TIFR0 |= (1<<TOV0);
								}
							}
							/* Get and return received data from buffer */
							return UDR1;
						}

						void usart_recieve_buffer_init()
						{
							usart_receive_buffer.head = NULL;
							usart_receive_buffer.tail = NULL;
						}

						bool usart_is_buffer_empty()
						{
							if (usart_receive_buffer.head == NULL) return true;
							else return false;
						}

						void usart_put_recieve(unsigned char in)
						{
							servo_parameter_t *new = create_servo_parameter(in);
							if (usart_is_buffer_empty())
								{
									usart_receive_buffer.head = new;
									usart_receive_buffer.tail = new;
								}
								else
									{
										usart_receive_buffer.tail->next = new;
										usart_receive_buffer.tail = new;
									}
								}

								unsigned char usart_pop_recieve( void )
								{
									int val = -1;
									ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
									{
										if (usart_receive_buffer.head != NULL)
											{
												servo_parameter_t *h = usart_receive_buffer.head;
												val = h->current_parameter;
												usart_receive_buffer.head = h->next;
												free(h);
											}
										}
										return val;
									}

									void usart_flush_rx()
									{
										UCSR1B = (0<<RXEN1)|(1<<TXEN1);
										UCSR1B = (1<<RXEN1)|(1<<TXEN1);
									}

									void usart_set_tx(){
										ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
										{
											usart_flush_rx();
											/* Turn off rx */
											PORTB |= 0x01; //00000001
											/* Turn on tx */
											PORTB &= 0xFD; //11111101
										}
									}

									void usart_set_rx()
									{
										ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
										{
											///* Reset counter and counter-flag */
											//TCNT0 = 0x00;
											//TIFR0 |= (1<<TOV0);
											//int timeout = 0;
											/////* Wait for data to be shifted out */
											//while ( !( UCSR1A & (1<<TXC1)) )
											//{
											///* If time out, return NULL */
											//if (TIFR0 & (1<<TOV0))
											//{
											//if (timeout > 3)
											//{
											//return 0x34;
											//}
											//timeout++;
											//TIFR0 |= (1<<TOV0);
											//}
											//}
											//UCSR1A |= (1<<TXC1); // Reset flag
											/* Turn off tx */
											PORTB |= 0x02; //00000010
											/* Turn on rx */
											PORTB &= 0xFE; //11111110
										}
									}

									void usart_disconnect(){
										/* Wait for data to be shifted out */
										while ( !( UCSR1A & (1<<TXC1)) );
											PORTB |= 0x03; //00000011
										}
