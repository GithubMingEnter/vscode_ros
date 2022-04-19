#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/lwm/vscode_ros/src/turtlebot/turtlebot3-melodic-devel/turtlebot3_teleop"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/lwm/vscode_ros/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/lwm/vscode_ros/install/lib/python2.7/dist-packages:/home/lwm/vscode_ros/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/lwm/vscode_ros/build" \
    "/usr/bin/python2" \
    "/home/lwm/vscode_ros/src/turtlebot/turtlebot3-melodic-devel/turtlebot3_teleop/setup.py" \
     \
    build --build-base "/home/lwm/vscode_ros/build/turtlebot/turtlebot3-melodic-devel/turtlebot3_teleop" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/lwm/vscode_ros/install" --install-scripts="/home/lwm/vscode_ros/install/bin"
