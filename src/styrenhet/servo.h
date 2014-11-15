/*
 * servo.h
 *
 * Created: 2014-11-08 17:52:50
 * Description: Functions for the servo ax-12a.
 */ 

#ifndef SERVO_H_
#define SERVO_H_

#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include <avr/io.h>
#include "ax12a.h"

/* Following datatypes represents an instruction, meant to be sent to our servo.
	The datatype is designed to be sent in a single batch. */
typedef struct servo_parameter
{
	uint8_t current_parameter;
	struct servo_parameter *next;
} servo_parameter_t;

typedef struct servo_instruction
{
	servo_parameter_t *first_parameter;
	servo_parameter_t *last_parameter;
	/* Number of parameters */
	int length;
} servo_instruction_t;

/* Functions performing the actual sending of data to servo via UART */
void servo_init(int ID);
void send_servo_instruction(servo_instruction_t *t);

/* Functions for creating servo instructions from data */
servo_instruction_t* servo_instruction_packet(int ID, int instr, int reg, servo_parameter_t *parameters);
uint8_t make_checksum(uint8_t ID, uint8_t length, uint8_t instr, uint8_t parameters);

/* Functions for handling servo_instructions */
servo_instruction_t* create_instructions(int amount);
servo_instruction_t* concatenate_instructions(servo_instruction_t *t1, servo_instruction_t *t2);
void free_instruction(servo_instruction_t *t);
void free_instruction_full(servo_instruction_t *t);

/* Following functions handle the parameters which are the single bytes
	an instruction is made up of */
servo_parameter_t* create_servo_parameter(unsigned int new_parameter);
void add_servo_parameter(servo_instruction_t *instr, unsigned int new_parameter);
servo_parameter_t* get_servo_parameter(servo_instruction_t *instr);
servo_parameter_t* next_servo_parameter(servo_parameter_t *p);
bool empty_servo_parameter(servo_parameter_t *p);
servo_parameter_t* last_servo_parameter(servo_parameter_t *p);
unsigned int servo_parameter_value(servo_parameter_t *p);
int servo_parameter_sum(servo_parameter_t *p);

/* Functions for handling chains of parameters */
void add_servo_parameter_chain(servo_parameter_t *t, uint8_t new_data);
void free_servo_parameter_chain(servo_parameter_t *p);
int servo_parameter_chain_length(servo_parameter_t *p);

#endif /* SERVO_H_ */