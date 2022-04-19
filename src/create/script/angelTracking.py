#!/usr/bin/python
# coding=utf-8

from glob import glob
import rospy
import math
from geometry_msgs.msg import Twist,Point,Quaternion
from nav_msgs.msg import Odometry
import sys, select, termios, tty
import PID
msg = """
angular control
"""
angular_z=0
or_z=0
Tor_w=Quaternion()
curPos=Point()
curOr=Quaternion()
minAngular=0.05
maxAngular=2
def getT265_callback(data):
    global angular_z ,or_z,Tor_w
    or_z=data.pose.pose.orientation.z
    angular_z=data.twist.twist.angular.z
    Tor_w=data.pose.pose.orientation
    # Tor_w.z=-0.6
    # rospy.loginfo("angular_z=%f",angular_z)
    # rospy.loginfo("or_z=%f",Tor_w.z)
    # rospy.loginfo("or_w=%f",Tor_w.w)

def get_odom(data):
    global curPos,curOr
    curPos=data.pose.pose.position
    curOr=data.pose.pose.orientation

def cmd_vel_pub():
    rospy.init_node("t265ControlAngular")
    cmd_pub=rospy.Publisher('cmd_vel',Twist,queue_size=10)
    odom_sub=rospy.Subscriber('/cameraT265/odom/sample',Odometry,getT265_callback)
    RobotOdom_sub=rospy.Subscriber('odom',Odometry,get_odom)
    control_speed = 0 #前进后退实际控制速度
    control_turn  = 0 #转向实际控制速度
    targetOr=0# 转向控制角度
    rate = rospy.Rate(10) 
    
    rospy.loginfo("start control t265")
    try:
        while not rospy.is_shutdown():
            startOr=curOr
            while True:
                twist = Twist() #创建ROS control话题变量
                
                errorOr=Tor_w.z-curOr.z
                rospy.loginfo("errorOr=%f",errorOr)
                if errorOr>=0:
                    twist.angular.z=2*errorOr


                    if twist.angular.z<minAngular:
                        twist.angular.z=0
                    elif twist.angular.z>maxAngular:
                        twist.angular.z=maxAngular
                    else:
                        pass
                    rospy.loginfo("twist.angular.z=%f",twist.angular.z)
                    cmd_pub.publish(twist)
                else:
                    twist.angular.z=-2*errorOr
                    if twist.angular.z<minAngular:
                        twist.angular.z=0
                    elif twist.angular.z>maxAngular:
                        twist.angular.z=maxAngular
                    else:
                        pass
                    twist.angular.z*=-1
                    rospy.loginfo("twist.angular.z=%f",twist.angular.z)
                    cmd_pub.publish(twist)
                    
                # rate.sleep()
    #运行出现问题则程序终止并打印相关错误信息
    except Exception as e:
        print(e)
    #程序结束前发布速度为0的速度话题
    finally:
        twist = Twist()
        twist.linear.x = 0;  twist.linear.y = 0;  twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        cmd_pub.publish(twist)

if __name__ == "__main__":
    try:
        cmd_vel_pub()
    except rospy.ROSInterruptException:
        pass