/*
 * armlib.h
 *
 * Created: 2014-11-08 17:52:50
 * Description: Functions for arm.
 */ 

#ifndef ARMLIB_H_
#define ARMLIB_H_

typedef struct servo_data
{
	unsigned int speed;
	unsigned int position;
	unsigned int goal_speed;
	unsigned int goal_position;
} servo_data_t;

typedef struct arm_data
{
	servo_data_t *s;
	int length;
} arm_data_t;

typedef struct parameter
{
	unsigned int current_parameter;
	parameter *next;
} parameter_t;

typedef struct arm_instruction
{
	unsigned int address;
	unsigned int instruction;
	parameter *parameters;
	/* Number of parameters */
	int length;
} arm_instruction_t;

arm_data_t* new_arm_data(int number_of_servos);
void free_arm_data(arm_data_t *arm);
void set_servo_speed(arm_data_t *arm, int servo, unsigned int new_speed);
void set_servo_position(arm_data_t *arm, int servo, unsigned int new_position);
int get_servo_speed(arm_data_t *arm, int servo);
int get_servo_position(arm_data_t *arm, int servo);
void set_servo_goal_speed(arm_data_t *arm, int servo, unsigned int new_speed);
void set_servo_goal_position(arm_data_t *arm, int servo, unsigned int new_position);
int get_servo_goal_speed(arm_data_t *arm, int servo);
int get_servo_goal_position(arm_data_t *arm, int servo);
arm_instruction_t* create_instruction();
void add_instruction(arm_instruction_t *instr, unsigned int new_instruction);
void add_address(arm_instruction_t *instr, unsigned int new_address);
void add_parameter(arm_instruction_t *instr, unsigned int new_parameter);
parameter_t* get_parameter(arm_instruction_t *instr);
parameter_t* next_parameter(parameter_t *p);
parameter_t* create_parameter(unsigned int new_parameter);
bool empty_parameter(parameter_t *p);
parameter_t* last_parameter(parameter_t *p);
unsigned int parameter_value(parameter_t *p);

#endif /* ARMLIB_H_ */