/*
 * parameter_chain.h
 *
 * Created: 2014-11-08 17:52:50
 * Description: Functions for handling a linked list containing
 * 				parameters (in this case uint8_t)
 */ 

#ifndef PARAMETER_CHAIN_H
#define PARAMETER_CHAIN_H

#include <stdlib.h>
#include <stddef.h>
#include <avr/io.h>
#include <stdbool.h>

typedef struct servo_parameter
{
	uint8_t current_parameter;
	struct servo_parameter *next;
} servo_parameter_t;

/* Functions for handling individual servo_parameter_t */
servo_parameter_t* create_servo_parameter(unsigned int new_parameter);
servo_parameter_t* next_servo_parameter(servo_parameter_t *p);
bool empty_servo_parameter(servo_parameter_t *p);
servo_parameter_t* last_servo_parameter(servo_parameter_t *p);
unsigned int servo_parameter_value(servo_parameter_t *p);
int servo_parameter_sum(servo_parameter_t *p);
void set_parameter_next(servo_parameter_t *this, servo_parameter_t *next);

/* Functions for handling chains of parameters */
void add_servo_parameter_chain(servo_parameter_t *t, uint8_t new_data);
void free_servo_parameter_chain(servo_parameter_t *p);
int servo_parameter_chain_length(servo_parameter_t *p);

#endif /* SERVO_H_ */