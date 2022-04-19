#!/usr/bin/python
# encoding:utf-8

from itertools import count
import rospy
import numpy as np

from geometry_msgs.msg import PointStamped
from visualization_msgs.msg import MarkerArray
from visualization_msgs.msg import Marker
class Turtlebot_core():
    def __init__(self):
        rospy.init_node("TurtlebotPoint",anonymous=True)
        self.buf=[]
        self.count=0
        # self.id=0
        self.mark_pub    = rospy.Publisher('/path_point', MarkerArray, queue_size = 100) #用于发布marker point
        self.markerArray=MarkerArray()
        self.markerArray_num=MarkerArray()
        rospy.Subscriber("/clicked_point",PointStamped,self.bufCallback,queue_size=1)
        rospy.spin()
        
    def bufCallback(self,data):
        p1=np.zeros(2)
        p1[0]=data.point.x
        p1[1]=data.point.y
        self.count+=1
        # self.id+=1
        self.markerClick(data)
        self.buf.append(p1)
        np.savetxt("line.txt",np.array(self.buf))
        print("save successfully")
        print("P:"+str(p1))


    def markerClick(self,data):
        # print('Add a new target point '+str(count)+':')
        # print('x:'+str(data.point.x)+
        # ', y:'+str(data.point.y)+
        # ', z:0'+', w:1') 
        marker = Marker()      #创建marker对象
        marker.header.frame_id = 'map' #以哪一个TF坐标为原点
        marker.type = marker.ARROW #一直面向屏幕的字符格式
        marker.action = marker.ADD #添加marker
        marker.scale.x = 0.2 #marker大小
        marker.scale.y = 0.05 #marker大小
        marker.scale.z = 0.05 #marker大小，对于字符只有z起作用
        marker.color.a = 1 #字符透明度
        marker.color.r = 1 #字符颜色R(红色)通道
        marker.color.g = 0 #字符颜色G(绿色)通道
        marker.color.b = 0 #字符颜色B(蓝色)通道
        marker.pose.position.x = data.point.x #字符位置
        marker.pose.position.y = data.point.y #字符位置
        marker.pose.orientation.z = 0 #字符位置
        marker.pose.orientation.w = 1 #字符位置
        self.markerArray.markers.append(marker) #添加元素进数组

        marker_number = Marker()      #创建marker对象
        marker_number.header.frame_id = 'map' #以哪一个TF坐标为原点
        marker_number.type = marker_number.TEXT_VIEW_FACING #一直面向屏幕的字符格式
        marker_number.action = marker_number.ADD #添加marker
        marker_number.scale.x = 0.5 #marker大小
        marker_number.scale.y = 0.5 #marker大小
        marker_number.scale.z = 0.5 #marker大小，对于字符只有z起作用
        marker_number.color.a = 1 #字符透明度
        marker_number.color.r = 1 #字符颜色R(红色)通道
        marker_number.color.g = 0 #字符颜色G(绿色)通道
        marker_number.color.b = 0 #字符颜色B(蓝色)通道
        marker_number.pose.position.x = data.point.x #字符位置
        marker_number.pose.position.y = data.point.y #字符位置
        marker_number.pose.position.z = 0.1 #字符位置
        marker_number.pose.orientation.z = 0 #字符位置
        marker_number.pose.orientation.w = 1 #字符位置
        marker_number.text = str(count) #字符内容
        self.markerArray_num.markers.append(marker_number) #添加元素进数组

        #markers的id不能一样，否则rviz只会识别最后一个元素
        id = 0
        for m in self.markerArray.markers:    #遍历marker分别给id赋值
            m.id = id
            id += 1

        for m in self.markerArray_num.markers:    #遍历marker分别给id赋值
            m.id = id
            id += 1
        
        self.mark_pub.publish(self.markerArray) #发布markerArray，rviz订阅并进行可视化
        self.mark_pub.publish(self.markerArray_num) #发布markerArray，rviz订阅并进行可视化


if __name__=="__main__":
    turtlebot_core=Turtlebot_core()


