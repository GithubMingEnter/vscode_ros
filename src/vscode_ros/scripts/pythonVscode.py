#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
    Python 版本的 HelloVScode，执行在控制台输出 HelloVScode
    实现:
    1.导包
    2.初始化 ROS 节点
    3.日志输出 
"""
 
import  rospy # 1.导包
 
if __name__ == "__main__":
 
    rospy.init_node("Hello_Vscode_p")  # 2.初始化 ROS 节点
    rospy.loginfo("gogo")
    rospy.loginfo("Hello VScode, I am Python ....")  #3.日志输出 Hello vscode
