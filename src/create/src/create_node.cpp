#include "ros/ros.h"

//msg includes
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/PoseWithCovarianceStamped.h>
#include "std_msgs/String.h"
// %EndTag(MSG_HEADER)%

#include <sstream>
ros::Publisher pose_pub;

void poseCallback( const nav_msgs::Odometry::ConstPtr& pose_msg)
{

  //object for storing the pose data
  geometry_msgs::PoseWithCovarianceStamped pose;

  pose.header = pose_msg->header;
  pose.pose = pose_msg->pose;
  pose_pub.publish(pose);
}

int main(int argc, char **argv)
{
  //Ros node initializations
  ros::init(argc, argv, "extract_pose");
  ros::NodeHandle nh;

  //Publisher object
  pose_pub = nh.advertise<geometry_msgs::PoseWithCovarianceStamped>("pose", 1000);

  //Subscriber object
  ros::Subscriber odom_sub = nh.subscribe("odometry/filtered", 1000, poseCallback);
  ROS_INFO("GO GO TO CREATE");
  ros::spin();

  return 0;
}