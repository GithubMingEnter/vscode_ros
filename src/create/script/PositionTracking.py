#!/usr/bin/env python
# coding=gbk

import rospy
import tf
import actionlib
import move_base_msgs.msg as moveMsg
import visualization_msgs.msg as vizMsg
import std_msgs.msg as std_msgs
import geometry_msgs.msg as geometry_msgs



class TourMachine(object):
    def __init__(self,repeat=False): 
        action_name='move_base'
        self._ac_move_base=actionlib.SimpleActionClient(action_name,
                                                                                                                    moveMsg.MoveBaseAction)
        rospy.loginfo('wait for %s server'% action_name)
        while self._ac_move_base.wait_for_server(rospy.Duration(5))==False:
            rospy.loginfo("Waiting for the move_base action server to come up")
        

        self._counter=0
        self._repeat=repeat
        self._pub_viz_marker=rospy.Publisher('viz_waypoint',vizMsg.MarkerArray,queue_size=1,latch=True)
        self.target = geometry_msgs.PoseStamped()
    def move_to_next(self,goalX, goalY ,goalW):
        rospy.loginfo("send goal")
        p=self._get_next_destination(goalX, goalY ,goalW)
        rospy.loginfo("goalX=%f ,goalY=%f, goalW=%f ",goalX, goalY ,goalW)
        self._ac_move_base.send_goal(p)
        self._ac_move_base.wait_for_result()
        result=self._ac_move_base.get_result()
        rospy.loginfo("result:%s"%result)
        # if(self._ac_move_base.get_state()==actionlib.SimpleGoalState))
        return True

    def _get_next_destination(self,goalX,goalY,goalW):
        self._counter=0
        self.target.header.frame_id="map"
        self.target.header.stamp=rospy.Time.now()#ros::Time::now()
        self.target.pose.position.x=goalX
        self.target.pose.position.y=goalY
        # self.target.pose.orientation.z=0.02
        self.target.pose.orientation.w=goalW
        goal=moveMsg.MoveBaseGoal(self.target)
        return goal

    def spin(self):
        rospy.sleep(1.0)
        finished=False
        while not rospy.is_shutdown() and not finished:
            finished=self.move_to_next()
            rospy.sleep(2.0)

# if __name__ == '__main__':
#     rospy.init_node('tour')
#     tourMachine=TourMachine()
#     rospy.loginfo('Initialized')
#     tourMachine.spin()
#     rospy.loginfo('Bye Bye')

