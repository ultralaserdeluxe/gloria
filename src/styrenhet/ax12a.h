//--- Control Table Address ---
//EEPROM AREA 
//--- Addresses ---
#define P_MODEL_NUMBER_L 0x00
#define P_MODOEL_NUMBER_H 0x01
#define P_VERSION 0x02
#define P_ID 0x03
#define P_BAUD_RATE 0x04
#define P_RETURN_DELAY_TIME 0x05
#define P_CW_ANGLE_LIMIT_L 0x06
#define P_CW_ANGLE_LIMIT_H 0x07
#define P_CCW_ANGLE_LIMIT_L 0x08
#define P_CCW_ANGLE_LIMIT_H 0x09
#define P_SYSTEM_DATA2 0x0A
#define P_LIMIT_TEMPERATURE 0x0B
#define P_DOWN_LIMIT_VOLTAGE 0x0C
#define P_UP_LIMIT_VOLTAGE 0x0D
#define P_MAX_TORQUE_L 0x0E
#define P_MAX_TORQUE_H 0x0F
#define P_RETURN_LEVEL 0x10
#define P_ALARM_LED 0x11
#define P_ALARM_SHUTDOWN 0x12
#define P_OPERATING_MODE 0x13
#define P_DOWN_CALIBRATION_L 0x14
#define P_DOWN_CALIBRATION_H 0x15
#define P_UP_CALIBRATION_L 0x16
#define P_UP_CALIBRATION_H 0x17
#define P_TORQUE_ENABLE 0x18
#define P_LED 0x19
#define P_CW_COMPLIANCE_MARGIN 0x1A
#define P_CCW_COMPLIANCE_MARGIN 0x1B
#define P_CW_COMPLIANCE_SLOPE 0x1C
#define P_CCW_COMPLIANCE_SLOPE 0x1D
#define P_GOAL_POSITION_L 0x1E
#define P_GOAL_POSITION_H 0x1F
#define P_GOAL_SPEED_L 0x20
#define P_GOAL_SPEED_H 0x21
#define P_TORQUE_LIMIT_L 0x22
#define P_TORQUE_LIMIT_H 0x23
#define P_PRESENT_POSITION_L 0x24
#define P_PRESENT_POSITION_H 0x25
#define P_PRESENT_SPEED_L 0x26
#define P_PRESENT_SPEED_H 0x27
#define P_PRESENT_LOAD_L 0x28
#define P_PRESENT_LOAD_H 0x29
#define P_PRESENT_VOLTAGE 0x2A
#define P_PRESENT_TEMPERATURE 0x2B 
#define P_REGISTERED_INSTRUCTION 0x2C
#define P_PAUSE_TIME 0x2D
#define P_MOVING 0x2E
#define P_LOCK 0x2F
#define P_PUNCH_L 0x30
#define P_PUNCH_H 0x31

//--- Init values ---
#define P_CW_ANGLE_LIMIT_L_INIT 0x00
#define P_CW_ANGLE_LIMIT_H_INIT 0x00
#define P_CCW_ANGLE_LIMIT_L_INIT 0xFF
#define P_CCW_ANGLE_LIMIT_H_INIT 0x03
#define P_CW_COMPLIANCE_MARGIN_INIT 0x00
#define P_CCW_COMPLIANCE_MARGIN_INIT 0x00
#define P_CW_COMPLIANCE_SLOPE_INIT 0x20
#define P_CCW_COMPLIANCE_SLOPE_INIT 0x20
#define P_TORQUE_ENABLE_INIT ON
#define	P_RETURN_LEVEL_INIT 0x01
#define P_RETURN_DELAY_TIME_INIT 0x10
#define P_GOAL_SPEED_L_INIT 0x40
#define P_GOAL_SPEED_H_INIT 0x00
#define P_PUNCH_L_INIT 0x40
#define P_PUNCH_H_INIT 0x00
#define P_TORQUE_LIMIT_L_INIT 0xff
#define P_TORQUE_LIMIT_H_INIT 0x03
#define P_ALARM_SHUTDOWN_INIT 0x24
#define P_ALARM_LED_INIT 0x24

//--- Instruction ---
#define INSTR_PING 0x01
#define INSTR_READ 0x02
#define INSTR_WRITE 0x03
#define INSTR_REG_WRITE 0x04
#define INSTR_ACTION 0x05
#define INSTR_RESET 0x06
#define INSTR_DIGITAL_RESET 0x07
#define INSTR_SYSTEM_READ 0x0C
#define INSTR_SYSTEM_WRITE 0x0D
#define INSTR_SYNC_WRITE 0x83
#define INSTR_SYNC_REG_WRITE 0x8

 //--- Servos ---
#define SERVO_1 0x01
#define SERVO_2 0x02
#define SERVO_3 0x03
#define SERVO_4 0x04
#define SERVO_5 0x05
#define SERVO_6 0x06
#define SERVO_7 0x07
#define SERVO_8 0x08
#define SERVO_ALL 0xFE

//--- Servo max angle
#define SERVO_MAX_ANGLE_H 0x03
#define SERVO_MAX_ANGLE_L 0xff

//--- Joints ---
#define JOINT_1 0x00
#define JOINT_2 0x01
#define JOINT_3 0x02
#define JOINT_4 0x03
#define JOINT_5 0x04
#define JOINT_6 0x05

#define ON 0x01
#define OFF 0x00
#define _ON 0x00
#define _OFF 0x01

