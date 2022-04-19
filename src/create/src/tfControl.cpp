#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>
#include "sensor_msgs/LaserScan.h"
#include<geometry_msgs/Quaternion.h>

double angular_z = 0;    //通过计算得出的slave与master的角度
    //通过计算得出的slave与master的距离
double car_x=0;
double car_y=0;

double max_vel = 1;
double normal_vel = 0.5;

double max_ang=2.8;
double normal_ang=1.0;

double last_angular_z = 0;  
double last_car_x = 0;
double ddyz = 0;
double ddyx = 0;
double last_car_y = 0;
double ddyy = 0;
double plusandminus = 1.3;
// 增益系数调节
double Scalex_P = 0; 
double Scalex_I = 0;
double Scalez_P =0;
double Scalez_I =0;

// tf变换相关参数
std::string base_frame;
std::string base_to_car;
std::string base_to_camera;
std::string tf_prefix_;
float pose_x=0,pose_y=0,pose_z=0,speed_x=0,speed_y=0,speed_z=0;
geometry_msgs::Quaternion Tor;
void odom_callback1(const nav_msgs::Odometry::ConstPtr& msg)
{
    // float pose_x=0,pose_y=0,pose_z=0,speed_x=0,speed_y=0,speed_z=0;
    pose_x=msg->pose.pose.position.x;
    pose_y=msg->pose.pose.position.y;//note
    pose_z=msg->pose.pose.position.z;
    // speed_x=msg->twist.twist.linear.x;
    // speed_y=msg->twist.twist.linear.y;
    // speed_z=msg->twist.twist.linear.z;
    Tor=msg->pose.pose.orientation;
    // ROS_INFO("X:%f  Y:%f    Z:%f",pose_x,pose_y,pose_z);
    // ROS_INFO("Xv:%f  Yv:%f  Zv:%f",speed_x,speed_y,speed_z);


}

int main(int argc,char** argv)
{
    ros::init(argc,argv,"tfControl");
    ros::NodeHandle node;
    ros::NodeHandle private_nh("~");

    ros::Publisher slave_vel=node.advertise<geometry_msgs::Twist>("cmd_vel",10);
    ros::Subscriber cOdomSub=node.subscribe("/cameraT265/odom/sample",10,odom_callback1);
    //能不能转移到相对位置 的tf坐标


    private_nh.param<double>("Scalex_P", Scalex_P, 0);  
    private_nh.param<double>("Scalex_I", Scalex_I, 0);   
    private_nh.param<double>("Scalez_I", Scalez_I, 0);  
    private_nh.param<double>("Scalez_P", Scalez_P, 0);  
    

    private_nh.param<double>("max_vel", max_vel,0.4);  
    private_nh.param<double>("normal_vel", normal_vel,1); 
    // private_nh.param<double>("max_ang",max_ang,2.5);
    // private_nh.param<double>("normal_ang",normal_ang,1.0);

      private_nh.param<double>("plusandminus", plusandminus,1.3);  //判断为车在前方的阈值

    private_nh.param<std::string>("base_frame", base_frame, "map");
    private_nh.param<std::string>("base_to_car", base_to_car, "base_footprint");
    // private_nh.param<std::string>("base_to_slave", base_to_camera, "slave2");

     // 使用tf_prefix参数将frame_name解析为frame_id
     tf_prefix_=tf::getPrefixParam(private_nh);
     base_frame=tf::resolve(tf_prefix_,base_frame);
     base_to_car=tf::resolve(tf_prefix_,base_to_car);
    //   base_to_camera=tf::resolve(tf_prefix_,base_to_camera);

    tf::TransformListener listener;
    geometry_msgs::Twist vel_msg;

    ros::Rate rate(10.0);
    while(node.ok())
    {
        tf::StampedTransform transformBc;
        try{
            listener.waitForTransform(base_frame,base_to_car,ros::Time(0),ros::Duration(3.0));
            listener.lookupTransform(base_frame,base_to_car,ros::Time(0),transformBc);
        }
        catch (tf::TransformException &ex)
        {
            ROS_ERROR("%s",ex.what());
            ros::Duration(1.0).sleep();
            continue;
        }
        printf("x=%f, y=%f",transformBc.getOrigin().x(),transformBc.getOrigin().y());
        // car_x=sqrt(pow((transformBc.getOrigin().x()-pose_x), 2) +
        //                           pow((transformBc.getOrigin().y()-pose_y), 2));
        // angular_z = atan2((pose_y-transformBc.getOrigin().y()),
        //                            (pose_x-transformBc.getOrigin().x()));
        
            
        car_y=-transformBc.getOrigin().y()+pose_y;
        car_x= -transformBc.getOrigin().x()+pose_x;       
        angular_z=Tor.z-transformBc.getRotation().getZ();         
        printf("The distance bias= %f\n",car_x);    // 输出误差数据信息
        printf("The angle bias= %f\n",angular_z);     
        // if((car_x)<0) 
        //         car_x = -car_x;
        // if((car_y)<0) 
        //         car_y= -car_y;
        // if(angular_z<0)
        //         angular_z=-angular_z;
        ddyx = car_x - last_car_x ; 
        ddyz = angular_z - last_angular_z ;
        ddyy=car_y-last_car_y;
        //avoid static error
        //angular
        if(fabs(angular_z)>0.01)
        {
            vel_msg.angular.z=Scalex_P*angular_z;//Scalex_I*angular_z*angular_z+Scalex_P*ddyz;
             if(fabs(vel_msg.angular.z)>max_ang)
            {
                if(vel_msg.angular.z<0)
                    vel_msg.angular.z=-normal_ang;
                else
                    vel_msg.angular.z=normal_ang;

            }
            last_angular_z=angular_z;         
        }
        else
        {
            vel_msg.angular.z = 0;  
        }
        //position
        if (fabs(car_x)>0.08||fabs(car_y)>0.08)
        {
            vel_msg.linear.x=Scalex_I*car_x+Scalex_P*ddyx;
            vel_msg.linear.y=Scalex_I*car_y+Scalex_P*ddyy;
            
            // vel_msg.angular.z=Scalex_I*angular_z*angular_z+Scalex_P*ddyz;
            if(fabs(vel_msg.linear.x)>max_vel)
            {
                if(vel_msg.linear.x>0)
                    vel_msg.linear.x=normal_vel;
                else
                    vel_msg.linear.x=-normal_vel;
            }
            if(fabs(vel_msg.linear.y)>max_vel)
            {
                if(vel_msg.linear.y>0)
                    vel_msg.linear.y=normal_vel;
                else
                    vel_msg.linear.y=-normal_vel;
            }
            if(fabs(vel_msg.angular.z)>max_ang)
            {
                // if(vel_msg.angular.z<0)
                //      vel_msg.angular.z=-normal_ang;
                // else

                    // vel_msg.angular.z=normal_ang;

            }
            last_car_x=car_x;
            last_car_y=car_y;
            // last_angular_z=angular_z;

        }
        else
        {
            vel_msg.linear.x = 0;
            vel_msg.linear.y = 0;
            // vel_msg.angular.z = 0;    
        }
        ROS_INFO("vx= %f\n",vel_msg.linear.x);
        ROS_INFO("vy= %f\n",vel_msg.linear.y);
        ROS_INFO("vz= %f\n",vel_msg.angular.z);

        slave_vel.publish(vel_msg);
        ros::spinOnce();
        rate.sleep();
    }

    return 0;


}


