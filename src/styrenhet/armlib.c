/*
 * armlib.c
 *
 * Created: 2014-11-08 17:53:04
 * Description: Functions for the arm
 */ 

arm_data_t* new_arm_data(int number_of_servos)
{
	arm_data_t *this = malloc(arm_data_t);
	this->length = number_of_servos;
	this->s = malloc(number_of_servos * sizeof(servo_data_t))
	return this;
}

void free_arm_data(arm_data_t *arm)
{
	free(arm->s);
	free(arm);
}

void set_servo_speed(arm_data_t *arm, int servo, unsigned int new_speed)
{
	servo_data_t array = *(arm->s);
	array[servo].speed = new_speed;
}

void set_servo_position(arm_data_t *arm, int servo, unsigned int new_position)
{
	servo_data_t array = *(arm->s);
	array[servo].position = new_position;
}

int get_servo_speed(arm_data_t *arm, int servo)
{
	servo_data_t array = *(arm->s);
	return array[servo].speed;
}

int get_servo_position(arm_data_t *arm, int servo)
{
	servo_data_t array = *(arm->s);
	return array[servo].position;
}

void set_servo_goal_speed(arm_data_t *arm, int servo, unsigned int new_speed)
{
	servo_data_t array = *(arm->s);
	array[servo].goal_speed = new_speed;
}

void set_servo_goal_position(arm_data_t *arm, int servo, unsigned int new_position)
{
	servo_data_t array = *(arm->s);
	array[servo].goal_position = new_position;
}

int get_servo_goal_speed(arm_data_t *arm, int servo)
{
	servo_data_t array = *(arm->s);
	return array[servo].goal_speed
}

int get_servo_goal_position(arm_data_t *arm, int servo)
{
	servo_data_t array = *(arm->s);
	return array[servo].goal_position;
}

arm_instruction_t* create_instruction()
{
	arm_instruction_t *this = malloc(arm_instruction_t);
	this->length = 0;
	return this;
}

void add_instruction(arm_instruction_t *instr, unsigned int new_instruction)
{
	instr->instruction = new_instruction;
}

void add_address(arm_instruction_t *instr, unsigned int new_address)
{
	instr->instruction = new_address;
}

void add_parameter(arm_instruction_t *instr, unsigned int new_parameter)
{
	if (empty_parameter(instr->parameters))
	{
		instr->parameters = create_parameter(new_parameter);
	}
	else
	{
		parameter_t *last = last_parameter(instr->parameters);
		last->next = create_parameter(new_parameter);
	}
	instr->length++;
}

parameter_t* get_parameter(arm_instruction_t *instr)
{
	return instr->parameters;
}

parameter_t* next_parameter(parameter_t *p)
{
	return p->next;
}

parameter_t* create_parameter(unsigned int new_parameter)
{
	parameter_t *this = malloc(parameter_t);
	this->current_parameter = new_parameter;
	return this;
}

bool empty_parameter(parameter_t *p)
{
	if (p == NULL) return true;
	else return false;
}

parameter_t* last_parameter(parameter_t *p)
{
	if (p->next == NULL) return p;
	else
	{
		parameter_t *current = p;
		while (current->next != NULL)
		{
			current = current->next;
		}
		return current;
	}
}

unsigned int parameter_value(parameter_t *p)
{
	return p->current_parameter;
}