#!/usr/bin/env python
# coding=gbk

import rospy
import tf
import actionlib
import move_base_msgs.msg as moveMsg
import visualization_msgs.msg as vizMsg
import std_msgs.msg as std_msgs
import geometry_msgs.msg as geometry_msgs
from geometry_msgs.msg import Twist,Point,Quaternion
from nav_msgs.msg import Odometry
import math
import PositionTracking as PT
Tor_w=Quaternion()
Tpos=Point()
curPos=Point()

curOr=Quaternion()
def getT265_callback(data):
    global angular_z ,or_z,Tor_w,Tpos
    or_z=data.pose.pose.orientation.z
    angular_z=data.twist.twist.angular.z
    Tor_w=data.pose.pose.orientation
    Tpos=data.pose.pose.position

class VioRc(object):

    def __init__(self):
        self.AC=False
        
    def targetSend(self):
        pt=PT.TourMachine()
        # rospy.init_node("VioRc")
        odom_sub=rospy.Subscriber('/cameraT265/odom/sample',Odometry,getT265_callback)
        rate = rospy.Rate(10) 
        lastGoalX=Tpos.x
        lastGoalY=Tpos.y
        lastGoalW=Tor_w.w

        while not rospy.is_shutdown():
            #aiming at static error

            goalX=Tpos.x
            goalY=Tpos.y
            goalW=Tor_w.w
            # avoid 
            if abs(lastGoalW-goalW)>0.015 or abs(lastGoalX-goalX)>0.08 or abs(lastGoalY-goalY)>0.08:
                f=pt.move_to_next(goalX,goalY,goalW)
                lastGoalW=goalW
                lastGoalX=goalX
                lastGoalY=goalY

            rate.sleep()



if __name__ == "__main__":
    vioRc=VioRc()
    rospy.init_node("VioRc")
    try:
        vioRc.targetSend()
    except rospy.ROSInterruptException:
        pass





