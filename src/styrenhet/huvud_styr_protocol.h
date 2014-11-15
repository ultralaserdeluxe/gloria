/*
 * huvud_styr_protocol.h
 *
 * Created: 2014-11-14 16:00:55
 *  Author: Hannes
 */ 


#ifndef HUVUD_STYR_PROTOCOL_H_
#define HUVUD_STYR_PROTOCOL_H_

#define COMMAND_INSTRUCTION_MASK 0xF0
#define COMMAND_ADDRESS_MASK 0x0F
#define COMMAND_ACTION 0x

#define ADDRESS_ALL 0xF0
#define ADDRESS_ARM 0xD0
#define ADDRESS_JOINT_1 0x20
#define ADDRESS_JOINT_2 0x40
#define ADDRESS_JOINT_3 0x80
#define ADDRESS_JOINT_4 0xB0
#define ADDRESS_JOINT_5 0x00
#define ADDRESS_JOINT_6 0x00



#endif /* HUVUD_STYR_PROTOCOL_H_ */