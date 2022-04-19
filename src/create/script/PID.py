#!/usr/bin/python
# coding=utf-8

import time
import matplotlib
# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline
#这个程序的实质就是在前九秒保持零输出，在后面的操作中在传递函数为某某的系统中输出1

class PID_Postion:
    def __init__(self,P=2,I=0.0,D=0.0):
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.ControlTime=0
        self.currentTime=time.time()
        self.lastTime=self.currentTime
    

        self.clear()

    def clear(self):
        self.last_error=0.0
        self.IntError=0.0
        self.setPoint=0.0
        self.range=20.0
        self.output=0
        self.Pterm=0.0
        self.Iterm=0.0
        self.Dterm=0.0

    def update(self,feedbackValue):
        self.error=self.setPoint-feedbackValue
        self.currentTime=time.time()
        deltaTime=self.currentTime-self.lastTime
        deltaError=self.error-self.last_error
        if deltaTime>=self.ControlTime:
            
            self.Pterm=self.error
            self.Iterm+=self.error*deltaTime

            if(self.Iterm<-self.range):
                self.Iterm=-self.range
            elif(self.Iterm>self.range):
                self.Iterm=self.range
            if deltaTime>0:
                self.Dterm=deltaError/deltaTime
            self.last_error=self.error
            self.lastTime=self.currentTime
            self.output=self.Pterm*self.Kp+self.Iterm*self.Ki+self.Dterm*self.Kd
    def setSampleTime(self, sample_time):
            self.ControlTime = sample_time

class PID_Increment:
    def __init__(self,P=2,I=0.0,D=0.0):
        self.Kp=P
        self.Ki=I
        self.Kd=D
        self.ControlTime=0.0
        self.currentTime=time.time()
        self.lastTime=self.currentTime
        
        self.clear()

    def clear(self):
        self.last_error=0.0
        self.IntError=0.0
        self.setPoint=0.0
        self.previousError=0.0
        self.range=3
        self.output=0
        self.Pterm=0.0
        self.Iterm=0.0
        self.Dterm=0.0

    def update(self,feedbackValue):
        self.error=self.setPoint-feedbackValue
        self.currentTime=time.time()
        deltaTime=self.currentTime-self.lastTime
        if deltaTime>self.ControlTime:
            self.Pterm=self.Kp*(self.error-self.last_error)
            self.Iterm=self.Ki*self.error
            self.Dterm=self.Kd*(self.error-2*self.last_error+self.previousError)
            self.previousError=self.last_error
            self.last_error=self.error
            self.lastTime=self.currentTime
            self.output=self.Pterm+self.Iterm+self.Dterm
    def setSampleTime(self, sample_time):
            self.ControlTime = sample_time


def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
    """Self-test PID class

    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    pid = PID_Increment(P, I, D)
    # pid = PID(P, I, D)
    pid.setPoint=0.0
    
    pid.setSampleTime(0.01)

    END = L
    feedback = 0

    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        if pid.setPoint > 0:
            feedback +=output# (output - (1/i))控制系统的函数
        if i>3:
            pid.setPoint = 1
        time.sleep(0.01)

        feedback_list.append(feedback)
        setpoint_list.append(pid.setPoint)
        time_list.append(i)

    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
    feedback_smooth = spline(time_list, feedback_list, time_smooth)
    plt.figure(0)
    plt.plot(time_smooth, feedback_smooth)
    plt.plot(time_list, setpoint_list)
    plt.xlim((0, L))
    plt.ylim((min(feedback_list)-0.5, max(feedback_list)+0.5))
    plt.xlabel('time (s)')
    plt.ylabel('PID (PV)')
    plt.title('TEST PID')

    # plt.ylim((1-0.5, 1+0.5))

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test_pid(0.8, 0.1, 0.001, L=80)
    



