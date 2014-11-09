/*
 * command_queue.c
 *
 * Created: 2014-11-08 14:57:57
 * Description: Datatype queue, meant to store commands
 */ 

#include "command_queue.h"

/* Create a new queue, with one empty entry */
queue_t* new_queue()
{
	queue_t *this = malloc(sizeof(queue_t));
	this->head = NULL;
	this->last = NULL;
	return this;
}

void free_queue(queue_t *q)
{
	queue_node_t *current;
	while(q->head != NULL)
	{
		current = q->head;
		q->head = current->next;
		free_node(current);
	}
	free(q);
}

/* Add new node to end of queue */
void put_queue(queue_t *q, queue_node_t *node)
{
	if (empty_queue(q))
	{
		q->head = node;
		q->last = node;
	}
	else
	{
		q->last->next = node;
		q->last = node;
	}
}

/* Remove and return first entry */
queue_node_t* pop_first(queue_t *q)
{
	queue_node_t *node = q->head;
	q->head = node->next;
	return node;
}

/* Remove node *node from queue */
void remove_node(queue_t *q, queue_node_t *node)
{
	if (empty_queue(q))
	{
		return;
	}
	
	queue_node_t *current = q->head;
	if (node == first_node(q))
	{
		q->head = node->next;
		current = q->head;
	}
	else
	{
		while (current->next != node)
		{
			if (current->next == NULL)
			{
				/* Node not in queue */
				return;
			}
			current = current->next;
		}
		current->next = node->next;
	}
	
	if (node == last_node(q))
	{
		q->last = current;
	}
}

bool empty_queue(queue_t *this)
{
	if (this->head == NULL)
	{
		return true;
	}
	else
	{
		return false;
	}
}

queue_node_t* first_node(queue_t *this)
{
	return this->head;
}

queue_node_t* last_node(queue_t *this)
{
	return this->last;
}

queue_node_t* next_node(queue_node_t *node)
{
	return node->next;
}

/* Returns a new node */
queue_node_t* new_node()
{
	queue_node_t *this;
	this = malloc(sizeof(queue_node_t));
	this->command = new_command();
	return this;
}

/* Frees node and returns pointer to next node */
queue_node_t* free_node(queue_node_t* this)
{
	queue_node_t *next_node = this->next;
	free(this->command);
	free(this);
	return next_node;
}

command_struct_t* node_data(queue_node_t *node)
{
	return node->command;
}

/* Abstraction wrapper for set_command */
int set_node_command(queue_node_t *node, int chooser, int data)
{
	return set_command(node->command, chooser, data);
}

/* Sets a part of command command, chosen with chooser to data. 
	Returns updated status */
int set_command(command_struct_t *command, int chooser, int data)
{
	switch (chooser)
	{
		case 0 :
			command->instruction = data;
			command->status++;
			return command->status;
		case 1 :
			command->data_1 = data;
			command->status++;
			return command->status;
		case 2 :
			command->data_2 = data;
			command->status++;
			return command->status;
		default:
			/* Invalid call */
			return NULL;
	}
}

/* Returns a new command struct with status = 0, others null */
command_struct_t* new_command()
{
	command_struct_t *this;
	this = malloc(sizeof(command_struct_t));
	this->status = 0;
	return this;
}

/* Returns current status */
int command_status(command_struct_t current)
{
	return current.status;
}
