import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import serial
import time
import numpy as np
import tkinter as tk
from tkinter import *
import pygubu
import os
import threading

ser = serial.Serial('COM4', 115200)

eulerAngles = [0.0 for i in range(3)]
regFactors = [0.0 for i in range(3)]
RW = [False for i in range(4)]
rbSel = 0


class testUI:
    def __init__(self):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('testUI.ui')

        #3: Create the mainwindow
        self.mainwindow = builder.get_object('topLevelFrame')
        #self.rb1Axis = builder.get_object('rb1Axis')
        #self.lblPsi = builder.get_object('lblPsi')
        #self.btnUpdate = builder.get_object('btnUpdate')

        self.enPsi = builder.get_object('enPsi')
        self.enTheta = builder.get_object('enTheta')
        self.enPhi = builder.get_object('enPhi')
        self.enKp = builder.get_object('enKp')
        self.enKi = builder.get_object('enKi')
        self.enKd = builder.get_object('enKd')

        #self.cbRW1 = builder.get_object('cbRW1')
        self.rw1State = builder.get_variable('rw1State')
        self.rw2State = builder.get_variable('rw2State')
        self.rw3State = builder.get_variable('rw3State')
        self.rw4State = builder.get_variable('rw4State')
        self.rbVar = builder.get_variable('rbVar')

        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def cmd(self):
        global eulerAngles
        global regFactors
        global RW
        global rbSel

        eulerAngles[0] = self.enPsi.get()
        eulerAngles[1] = self.enTheta.get()
        eulerAngles[2] = self.enPhi.get()
        regFactors[0] = self.enKp.get()
        regFactors[1] = self.enKi.get()
        regFactors[2] = self.enKd.get()
        RW[0] = self.rw1State.get()
        RW[1] = self.rw2State.get()
        RW[2] = self.rw3State.get()
        RW[3] = self.rw4State.get()

        rbSel = self.rbVar.get()

        print(rbSel)


def main():
    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    screen = pygame.display.set_mode((640, 480), video_flags)
    pygame.display.set_caption("PyTeapot IMU orientation visualization")

    resizewin(640, 480)
    init()
    frames = 0
    ticks = pygame.time.get_ticks()

    data = 0

    [omega, acc, magneto, dmp] = read_data()
    omega = [i * 250 * 2 * (np.pi / 180) / 65536 for i in omega]

    start_time = time.time()
    stop_time = time.time()

    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        [omega, acc, magneto, dmp] = read_data()
        omega = [i * 250*2*(np.pi/180)/65536 for i in omega]
        data += 1

        if time.time()-start_time >= 1.0:
            dt = time.time()-start_time
            start_time = time.time()
            print("{:.2f}".format(data/dt), " received/s")
            #print(omega, acc, magneto)

            print(dmp[0], dmp[1], dmp[2], dmp[3])
            data = 0

        magneto = magneto / np.linalg.norm(magneto)
        acc = acc / np.linalg.norm(acc)

        draw(dmp[0], dmp[1], dmp[2], dmp[3])

        pygame.display.flip()
        frames += 1

        
    print("fps: %d" % ((frames * 1000) / (pygame.time.get_ticks() - ticks)))
    ser.close()


def resizewin(width, height):
    """
    For resizing window
    """
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def cleanSerialBegin():
    try:
        line = ser.readline().decode('UTF-8').replace('\n', '')
        w = float(line.split('w')[1])
        nx = float(line.split('a')[1])
        ny = float(line.split('b')[1])
        nz = float(line.split('c')[1])
    except Exception:
        pass


def read_data():
    ser.reset_input_buffer()
    cleanSerialBegin()
    line = ser.readline().decode('UTF-8').replace('\n', '')

    wx = float(line.split(',')[0])
    wy = float(line.split(',')[1])
    wz = float(line.split(',')[2])
    ax = float(line.split(',')[3])
    ay = float(line.split(',')[4])
    az = float(line.split(',')[5])
    mx = float(line.split(',')[6])
    my = float(line.split(',')[7])
    mz = float(line.split(',')[8])

    qw = float(line.split(',')[9])
    qx = float(line.split(',')[10])
    qy = float(line.split(',')[11])
    qz = float(line.split(',')[12])

    omega = [wx, wy, wz]
    acc = [ax, ay, az]
    magneto = [mx, my, mz]
    quat = [qw, qx, qy, qz]

    return [omega, acc, magneto, quat]


def draw(w, nx, ny, nz):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)

    drawText((-2.6, 1.8, 2), "PyTeapot", 18)
    drawText((-2.6, 1.6, 2),
             "Module to visualize quaternion or Euler angles data", 16)
    drawText((-2.6, -2, 2), "Press Escape to exit.", 16)

    [yaw, pitch, roll] = quat_to_ypr([w, nx, ny, nz])
    drawText((-2.6, -1.8, 2),
             "Yaw: %f, Pitch: %f, Roll: %f" % (yaw, pitch, roll), 16)

    #just cry here
    glRotatef(2 * math.acos(w) * 180.00 / math.pi, nx, nz, -ny)     #Checked

    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(1.0, 0.2, 1.0)

    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(1.0, -0.2, -1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, -1.0)
    glEnd()


def drawText(position, textString, size):
    font = pygame.font.SysFont("Courier", size, True)
    textSurface = font.render(textString, True,
                              (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)


def quat_to_ypr(q):
    yaw = math.atan2(2.0 * (q[1] * q[2] + q[0] * q[3]),
                     q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3])
    pitch = -math.sin(2.0 * (q[1] * q[3] - q[0] * q[2]))
    roll = math.atan2(2.0 * (q[0] * q[1] + q[2] * q[3]),
                      q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3])
    pitch *= 180.0 / math.pi
    yaw *= 180.0 / math.pi
    yaw -= 2.598             # Declination at Sion
    roll *= 180.0 / math.pi
    return [yaw, pitch, roll]

if __name__ == '__main__':
    threading.Thread(target=main).start()
    app = testUI()
    app.run()