/*
 * command_queue.h
 *
 * Created: 2014-11-08 14:59:51
 * Description: Datatype queue, meant to store commands
 */ 
#ifndef COMMAND_QUEUE_H_
#define COMMAND_QUEUE_H_

#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include <avr/io.h>

typedef struct command_data
{
	uint8_t data;
	struct command_data next;
} command_data_t;

typedef struct command_struct
{
	uint8_t instruction;
	command_data_t data;
	
	/* Tells us if the full command has been recieved */
	int status;
} command_struct_t;

typedef struct queue_node
{
	command_struct_t *command;
	struct queue_node *next;
} queue_node_t;

typedef struct queue
{
	queue_node_t *head;
	queue_node_t *last;
} queue_t;

queue_t* new_queue();
void free_queue(queue_t *q);
void put_queue(queue_t *q, queue_node_t *node);
queue_node_t* pop_first(queue_t *q);
void remove_node(queue_t *q, queue_node_t *node);
bool empty_queue(queue_t *this);
queue_node_t* first_node(queue_t *this);
queue_node_t* last_node(queue_t *this);
queue_node_t* next_node(queue_node_t *node);
queue_node_t* new_node();
queue_node_t* free_node(queue_node_t* this);
command_struct_t* node_data(queue_node_t *node);
int set_node_command(queue_node_t *node, int chooser, int data);
int set_command(command_struct_t *command, int chooser, int data);
command_struct_t* new_command();
int command_status(command_struct_t current);

command_data_t* new_command_data(uint8_t new_data);
void add_command_data(command_struct_t *c, uint8_t new_data);
void free_command_data(command_struct_t *c)



#endif /* COMMAND_QUEUE_H_ */