/*
 * motor.h
 *
 * Created: 2014-11-14
 * Description: Functions for motor control.
 */ 


#ifndef MOTOR_H_
#define MOTOR_H_


typedef enum {FORWARD, BACKWARD, ROTATE_LEFT, ROTATE_RIGHT} direction_t;


void motor_init();
void set_speed(uint8_t speed);
void set_speed_left(uint8_t speed);
void set_speed_right(uint8_t speed);
void set_direction(direction_t direction);


#endif /* MOTOR_H_ */