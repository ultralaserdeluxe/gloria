/*
 * sensors.h
 *
 * Created: 2014-11-14
 * Description: Functions for working with the sensors.
 */

#ifndef SENSORS_H_
#define SENSORS_H_

#define line_sensor_first 0x00
#define line_sensor_last 0x0F

typedef struct sensor_data_t
{
	uint8_t line[15];
	uint8_t distance[2];
} sensor_data_t;

void read_linesensor(sensor_data_t* sensor_data);
void read_distance_left(sensor_data_t* sensor_data);
void read_distance_right(sensor_data_t* sensor_data);
void read_sensors(sensor_data_t* sensor_data);
sensor_data_t* sensors_init();


#endif /* SENSORS_H_ */
