# Description

## 安装测试librealsense SDK

参考[官网](https://github.com/IntelRealSense/librealsense/blob/master/doc/distribution_linux.md)完成安装，

如果需要在jetson上安装，可以参考这个[博客](https://blog.csdn.net/weixin_44000994/article/details/118441775?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2~default~CTRLIST~default-1.no_search_link&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2~default~CTRLIST~default-1.no_search_link)



启动realsense-viewer，看到下图所示窗口即完成安装

![](https://secure2.wostatic.cn/static/itLSxz7ZtPGYmup3Qs78po/image.png)



## realsense-ros安装

采用[源码](https://github.com/IntelRealSense/realsense-ros)安装，便于修改,特别是在一些坐标冲突时

```bash
mkdir -p  ~/vscode_ros/src
cd ~/vscode_ros/src

git clone https://github.com/IntelRealSense/realsense-ros.git
cd realsense-ros/
git checkout `git tag | sort -V | grep -P "^2.\d+\.\d+" | tail -1`  #查验
cd ..bash
catkin_make
echo "source ~/vscode_ros/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc


```



测试

```bash
roslaunch realsense2_camera rs_d400_and_t265.launch 

rviz
```

or

```bash
roslaunch realsense2_camera rs_camera.launch filters:=pointcloud
rviz
```

# instructions
followingRobot 存放的是被控移动机器人;
src目录下存放的是控制端;
做好ros多机通信后一定要先在主机中运行roscore

## motion planning method

人的相对位置就是移动机器人的导航目标点
```bash
roslaunch turn_on_wheeltec_robot navigation.launch
rviz -d navigation.rviz 
rosrun create ControlInt.py

```



## PID tracking method

查看坐标转换
`rosrun tf tf_echo "odom_combined" "base_footprint"`

记录人的坐标变换，进行跟随
```
roslaunch turn_on_wheeltec_robot navigation.launch
rviz -d navigation.rviz 
roslaunch create robot_tf.launch
```

