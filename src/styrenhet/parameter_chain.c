/*
 * parameter_chain.c
 *
 * Created: 2014-12-02 16:30:00
 * Description: Functions for handling a linked list containing
 * 				parameters (in this case uint8_t)
 */ 


servo_parameter_t* create_servo_parameter(unsigned int new_parameter)
{
	servo_parameter_t *this = malloc(sizeof(servo_parameter_t));
	this->current_parameter = new_parameter;
	this->next = NULL;
	return this;
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

/* Find the last parameter in a chain of parameters */
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

void set_parameter_next(servo_parameter_t *this, servo_parameter_t *next)
{
	this->next = next;
}

/* Functions specific for handling chains of parameters not part of a servo_instruction_t */
/* Add parameter to chain of parameters not part of a servo_instruction_t */
void add_servo_parameter_chain(servo_parameter_t *t, uint8_t new_data)
{
	if (t == NULL)
	{
		//t = create_servo_parameter(new_data);
		//t->next = NULL;
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
	servo_parameter_t *save;
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
	int length = 1;
	servo_parameter_t *current = p;
	while (current != NULL)
	{
		current = next_servo_parameter(current);
		length++;
		if (current->next == NULL)
		{
			return length;
		}
	}
	return length;
}