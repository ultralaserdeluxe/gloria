/*
 * servo.c
 *
 * Created: 2014-11-08 17:53:04
 * Description: Functions for a ax-12a servo.
 */ 

#include "servo.h"
#include "usart.h"

/* Initialize servo */
void servo_init(int ID)
{
		// Set baud to clk/16 => 1Mbps */
		usart_init();
		usart_set_tx();
		servo_parameter_t *p = NULL;
		
		add_servo_parameter_chain(p, P_CW_ANGLE_LIMIT_L_INIT);
		add_servo_parameter_chain(p, P_CW_ANGLE_LIMIT_H_INIT);
		add_servo_parameter_chain(p, P_CCW_ANGLE_LIMIT_L_INIT);
		add_servo_parameter_chain(p, P_CCW_ANGLE_LIMIT_H_INIT);
		send_servo_instruction(
			servo_instruction_packet(ID, INSTR_WRITE, P_CW_ANGLE_LIMIT_L, p)
		);
		
		free_servo_parameter_chain(p);
		
		add_servo_parameter_chain(p, P_CW_COMPLIANCE_MARGIN_INIT);
		add_servo_parameter_chain(p, P_CCW_COMPLIANCE_MARGIN_INIT);
		add_servo_parameter_chain(p, P_CW_COMPLIANCE_SLOPE_INIT);
		add_servo_parameter_chain(p, P_CCW_COMPLIANCE_SLOPE_INIT);
		send_servo_instruction(
			servo_instruction_packet(ID, INSTR_WRITE, P_CW_COMPLIANCE_MARGIN_INIT, p)
		);
		
		free_servo_parameter_chain(p);
		
		add_servo_parameter_chain(p, P_TORQUE_ENABLE_INIT);
		send_servo_instruction(
			servo_instruction_packet(ID, INSTR_WRITE, P_TORQUE_ENABLE, p)
		);
		
		free_servo_parameter_chain(p);
		
		add_servo_parameter_chain(p, P_RETURN_LEVEL_INIT);
		send_servo_instruction(
			servo_instruction_packet(ID, INSTR_WRITE, P_RETURN_LEVEL, p)
		);
		
		free_servo_parameter_chain(p);
		
		add_servo_parameter_chain(p, P_GOAL_SPEED_L_INIT);
		add_servo_parameter_chain(p, P_GOAL_SPEED_H_INIT);
		send_servo_instruction(
		servo_instruction_packet(ID, INSTR_WRITE, P_GOAL_SPEED_L, p)
		);
		
		free_servo_parameter_chain(p);
}

/* Does the actual sending of data to servo over UART*/
void send_servo_instruction(servo_instruction_t *t)
{
	servo_parameter_t *current = get_servo_parameter(t);
	while (!empty_servo_parameter(current))
	{
		usart_transmit(current->current_parameter);
		current = current->next;
	}
	//free_instruction_full(t);
}

/* Returns instruction for given parameters ready to be sent */
servo_instruction_t* servo_instruction_packet(int ID, int instr, int reg, servo_parameter_t *parameters)
{
	int length;
	if ((instr == INSTR_PING)||(instr == INSTR_ACTION)||(instr == INSTR_RESET))
	{
		length = 2; // 2 for instruction, checksum
	}
	else
	{
		length = servo_parameter_chain_length(parameters) + 3; // 3 for instruction, reg, checksum
	}
	servo_instruction_t *t = create_instructions(1);
	add_servo_parameter(t,0xFF);
	add_servo_parameter(t,0xFF);
	add_servo_parameter(t,ID);
	add_servo_parameter(t,length);
	add_servo_parameter(t,instr);
	if ((instr == INSTR_WRITE)||(instr == INSTR_REG_WRITE)||(instr == INSTR_READ))
	{
		add_servo_parameter(t,reg);
		servo_parameter_t *current = parameters;
		while (!empty_servo_parameter(current))
		{
			add_servo_parameter(t,servo_parameter_value(current));
			current = next_servo_parameter(current);
		}
	}
	add_servo_parameter(t,make_checksum(ID, length, instr, (reg + servo_parameter_sum(parameters))));
	return t;
}

/* Create checksum asked for from servo */
uint8_t make_checksum(uint8_t ID, uint8_t length, uint8_t instr, uint8_t parameters)
{
	return ~(ID + length + instr + parameters);
}

servo_instruction_t* create_instructions(int amount)
{
	servo_instruction_t *this = malloc(sizeof(servo_instruction_t)*amount);
	this->length = 0;
	return this;
}

servo_instruction_t* concatenate_instructions(servo_instruction_t *t1, servo_instruction_t *t2)
{
	t1->last_parameter->next = t2->first_parameter;
	t1->last_parameter = t2->last_parameter;
	free(t2);
	return t1;
}

void free_instruction(servo_instruction_t *t)
{
	free(t);
}

/* Free instruction and all parameters belonging to it */
void free_instruction_full(servo_instruction_t *t)
{
	servo_parameter_t *current = t->first_parameter;
	while(!empty_servo_parameter(current))
	{
		t->first_parameter = current->next;
		free(current);
		current = t->first_parameter;
	}
	free_instruction(t);
}

servo_parameter_t* create_servo_parameter(unsigned int new_parameter)
{
	servo_parameter_t *this = malloc(sizeof(servo_parameter_t));
	this->current_parameter = new_parameter;
	this->next = NULL;
	return this;
}

/* Add parameter to arm instruction */
void add_servo_parameter(servo_instruction_t *instr, unsigned int new_parameter)
{
	if (empty_servo_parameter(instr->first_parameter))
	{
		instr->first_parameter = create_servo_parameter(new_parameter);
		instr->last_parameter = instr->first_parameter;
	}
	else
	{
		servo_parameter_t *last = last_servo_parameter(instr->first_parameter);
		last->next = create_servo_parameter(new_parameter);
		instr->last_parameter = last->next;
	}
	instr->length++;
}

servo_parameter_t* get_servo_parameter(servo_instruction_t *instr)
{
	return instr->first_parameter;
}

servo_parameter_t* next_servo_parameter(servo_parameter_t *p)
{
	return p->next;
}

bool empty_servo_parameter(servo_parameter_t *p)
{
	if (p == NULL) return true;
	else return false;
}

servo_parameter_t* last_servo_parameter(servo_parameter_t *p)
{
	if (p->next == NULL) return p;
	else
	{
		servo_parameter_t *current = p;
		while (current->next != NULL)
		{
			current = current->next;
		}
		return current;
	}
}

unsigned int servo_parameter_value(servo_parameter_t *p)
{
	return p->current_parameter;
}

/* Return sum of parameters */
int servo_parameter_sum(servo_parameter_t *p)
{
	int sum = 0;
	servo_parameter_t *current = p;
	while (!empty_servo_parameter(current))
	{
		sum += servo_parameter_value(current);
		current = next_servo_parameter(current);
	}
	return sum;
}

/* Functions specific for handling chains of parameters not part of a servo_instruction_t */
/* Add parameter to chain of parameters not part of a servo_instruction_t */
void add_servo_parameter_chain(servo_parameter_t *t, uint8_t new_data)
{
	if (t == NULL)
	{
		t = create_servo_parameter(new_data);
		return;
	}
	servo_parameter_t *current = t;
	while (current->next != NULL)
	{
		current = next_servo_parameter(current);
	}
	current->next = create_servo_parameter(new_data);
}

/* Free a chain of parameters not part of a servo_instruction_t */
void free_servo_parameter_chain(servo_parameter_t *p)
{
	servo_parameter_t *current = p;
	servo_parameter_t *save = current->next;
	while (current != NULL)
	{
		save = current->next;
		free(current);
		current = save;
	}
}

/* Return length of chain of parameters not part of servo_instruction_t */
int servo_parameter_chain_length(servo_parameter_t *p)
{
	int length = 0;
	servo_parameter_t *current = p;
	while (current != NULL)
	{
		current = current->next;
		length++;
	}
	return length;
}

