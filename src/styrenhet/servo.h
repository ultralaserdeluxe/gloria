/*
 * servo.h
 *
 * Created: 2014-11-08 17:52:50
 * Description: Functions for the servo ax-12a.
 */ 

#ifndef SERVO_H_
#define SERVO_H_

#include "parameter_chain.h"

/* Following datatype is an instruction that is easy to iterate over 
	and send to a servo. */
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
servo_instruction_t* create_instruction();
servo_instruction_t* concatenate_instructions(servo_instruction_t *t1, servo_instruction_t *t2);
void free_instruction(servo_instruction_t *t);
void free_instruction_full(servo_instruction_t *t);

/* Following functions handle the servo_instruction_t */
void add_servo_parameter(servo_instruction_t *instr, unsigned int new_parameter);
servo_parameter_t* get_servo_parameter(servo_instruction_t *instr);

#endif /* SERVO_H_ */