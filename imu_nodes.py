#!/usr/bin/env python3

# Have to type the below line first for permission change to run
# sudo chmod a+rw /dev/i2c-*

import time
import board
import busio
import adafruit_icm20x
import rospy

from sensor_msgs.msg import Imu, MagneticField
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point, PointStamped, Pose, Quaternion, Twist, Vector3

import math
from math import sin, cos, pi
import tf

import numpy as np
from ahrs import filters


i2c = busio.I2C(board.SCL, board.SDA)
icm = adafruit_icm20x.ICM20948(i2c)


def talker():
    pub_imu = rospy.Publisher('example/imu', Imu, queue_size=50)
    pub_magfield = rospy.Publisher('example/magneticfield', MagneticField, queue_size=50)
    pub_marker = rospy.Publisher('example/marker', Marker, queue_size=50)
    pub_state = rospy.Publisher('example/state', PointStamped, queue_size=50)
    rospy.init_node('imu_node',anonymous=True)
    start_time = rospy.Time.now()
    current_time = rospy.Time.now()
    last_time = rospy.Time.now()
    rate = rospy.Rate(10) # 10hz while not rospy.is_shutdown(): odom = Odometry()

    frequency = 100       # frequency in Hz

    while not rospy.is_shutdown():

        #---------------------sensor_msgs/Imu---------------------------
        imu = Imu()
        imu.header.stamp = rospy.Time.now()
        imu.header.frame_id = 'base_link'

        # ORIENTATION
        madgwick = filters.Madgwick()
        Q = np.array([1.0, 0.0, 0.0, 0.0])

        acc_data = icm.acceleration # linear acceleration (m/s^2) x,y,z
        gyr_data = icm.gyro # angular velocity (rad/s) x,y,z
        mag_data = tuple(i for i in icm.magnetic) # magnetic field (uT) x,y,z

        madgwick.Dt = 1/frequency

        q = Quaternion()
        Q = madgwick.updateMARG(Q,acc=np.array(acc_data),gyr=np.array(gyr_data),mag=np.array(mag_data))
        q.w, q.x, q.y, q.z = Q

        # split values from gyro to geometry_msgs/Vector3
        v = Vector3()
        v.x, v.y, v.z = icm.gyro

        # split values from accelerometer to geometry_msgs/Vector3
        a = Vector3()
        a.x, a.y, a.z = icm.acceleration
        a.x, a.y, a.z = a.x, -a.y, a.z          # gravity pointing down
        #arrow.pose.position = state.point      # may adjust for S.R.G.S

        # store to geometry_msgs/Quaternion orientation
        imu.orientation = q
        # store to geometry_msgs/Vector3 angular_velocity
        imu.angular_velocity = v
        # store to geometry_msgs/Vector3 linear_velocity
        imu.linear_acceleration = a


        #---------------------sensor_msgs/MagneticField-----------------
        magfield = MagneticField()
        magfield.header.stamp = rospy.Time.now()
        magfield.header.frame_id = 'mag_link'

        # split values from magnetometer to geometry_msgs/Vector3
        h = Vector3()
        h.x, h.y, h.z = icm.magnetic

        # store to geometry_msgs/Vector3 linear_velocity
        magfield.magnetic_field = h		


        arrow = Marker()
        arrow.header.stamp = rospy.Time.now()
        arrow.header.frame_id = 'mark_link'
        arrow.type = 2
        arrow.color = (1,1,1,1)


        state = PointStamped()
        height = rospy.get_param("height",100)
        width = rospy.get_param("width",100)
        state.point.x = height
        state.point.y = width
        state.point.z = 20

        arrow.pose.position = state.point

        arrow.scale = h

        # print statements
        print()
        print("----------------------imu----------------------------")
        print()
        print(imu)
        #time.sleep(0.5)            # sleep for 0.5 seconds
        #print()
        #print("----------------------magfield-----------------------")
        #print()
        #print(magfield)
        #time.sleep(0.5)            # sleep for 0.5 seconds
        #print()
        #print("----------------------arrow--------------------------")
        #print()
        #print(arrow)
        #time.sleep(0.5)            # sleep for 0.5 seconds
        #print()
        #print("----------------------state--------------------------")
        #print()
        #print(state)

        time.sleep(0.5)             # sleep for 0.5 seconds

        pub_imu.publish(imu)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

