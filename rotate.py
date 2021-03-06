#!/usr/bin/env python2

import time
from math import radians, degrees, cos, sin

from OpenGL.GL import *
from OpenGL.GL.shaders import *

import pygame
from pygame.locals import *
import numpy    

width = 640
height = 480

vertices = numpy.array([-0.5, 0.5, 0.0,
                       -0.5, -0.5, 0.0,
                        0.5, -0.5, 0.0,
                        0.5,  0.5, 0.0,
                        -0.5, 0.5, -1.0,
                       -0.5, -0.5, -1.0,
                        0.5, -0.5, -1.0,
                        0.5,  0.5, -1.0], numpy.float32)
indices = numpy.array([0, 1, 2,
                       0, 2, 3,
                       0, 3, 7,
                       0, 7, 4,
                       0, 4, 5,
                       0, 5, 1,
                       3, 2, 6,
                       3, 6, 7], numpy.ushort)
colors = numpy.array([1.0, 1.0, 1.0, 1.0,
                      1.0, 0.0, 1.0, 1.0,
                      1.0, 0.0, 0.0, 1.0,
                      1.0, 1.0, 0.0, 1.0,
                      0.0, 1.0, 0.0, 1.0,
                      0.0, 1.0, 1.0, 1.0,
                      0.0, 0.0, 1.0, 1.0,
                      0.0, 0.0, 0.0, 1.0], numpy.float32)

modelview = numpy.identity(4, numpy.float32)

def getFileContents(filename):
    return open(filename, 'r').read()

def init():
    vertexShader = compileShader(getFileContents("rotate.vert"), GL_VERTEX_SHADER)
    fragmentShader = compileShader(getFileContents("rotate.frag"), GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, vertices)
    glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0, colors)

    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    glBindAttribLocation(program, 0, "a_Position")
    glBindAttribLocation(program, 1, "a_Color")

    glLinkProgram(program)

    global mvpLoc
    mvpLoc = glGetUniformLocation(program, "u_MVP")

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

    return program

xpos = 0.4
ypos = -0.23
zpos = 0.1

xrot = radians(56)
yrot = radians(150)
zrot = radians(38)

def drawWithoutVBOs():
    # Translate modelview
    modelview[3][0] = xpos
    modelview[3][1] = ypos
    modelview[3][2] = zpos

    # Rotate modelview
    modelview[0][0] = cos(yrot) * cos(zrot)
    modelview[1][0] = -cos(xrot) * sin(zrot) + sin(xrot) * sin(yrot) * cos(zrot)
    modelview[2][0] = sin(xrot) * sin(zrot) + cos(xrot) * sin(yrot) * cos(zrot)
    modelview[0][1] = cos(yrot) * sin(zrot)
    modelview[1][1] = cos(xrot) * cos(zrot) + sin(xrot) * sin(yrot) * sin(zrot)
    modelview[2][1] = -sin(xrot) * cos(zrot) + cos(xrot) * sin(yrot) * sin(zrot)
    modelview[0][2] = -sin(yrot)
    modelview[1][2] = sin(xrot) * cos(yrot)
    modelview[2][2] = cos(xrot) * cos(yrot)

    glUniformMatrix4fv(mvpLoc, 1, GL_FALSE, modelview)

    glDrawElementsus(GL_TRIANGLES, indices)

def main():
    pygame.init()
    pygame.display.set_mode((width, height), HWSURFACE | OPENGL | DOUBLEBUF)

    program = init()

    done = False
    xrot_delta = 0
    yrot_delta = 0
    zrot_delta = 0
    xpos_delta = 0
    ypos_delta = 0
    zpos_delta = 0
    global xrot
    global yrot
    global zrot
    global xpos
    global ypos
    global zpos

    while not done:
        glViewport(0, 0, width, height)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(program)
        drawWithoutVBOs()
        pygame.display.flip()
        xrot += radians(xrot_delta)
        yrot += radians(yrot_delta)
        zrot += radians(zrot_delta)
        xpos += xpos_delta
        ypos += ypos_delta
        zpos += zpos_delta
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
                elif event.key == K_p:
                    print "X, Y, Z:", xpos, ypos, zpos
                    print "Rotation:", degrees(xrot), degrees(yrot), degrees(zrot)
                elif event.key == K_q:
                    xrot_delta = 1
                elif event.key == K_a:
                    xrot_delta = -1
                elif event.key == K_w:
                    yrot_delta = 1
                elif event.key == K_s:
                    yrot_delta = -1
                elif event.key == K_e:
                    zrot_delta = 1
                elif event.key == K_d:
                    zrot_delta = -1
                elif event.key == K_LEFT:
                    xpos_delta = -0.01
                elif event.key == K_RIGHT:
                    xpos_delta = 0.01
                elif event.key == K_UP:
                    zpos_delta = 0.01
                elif event.key == K_DOWN:
                    zpos_delta = -0.01
                elif event.key == K_PAGEUP:
                    ypos_delta = 0.01
                elif event.key == K_PAGEDOWN:
                    ypos_delta = -0.01
            elif event.type == KEYUP:
                if event.key == K_q or event.key == K_a:
                    xrot_delta = 0
                elif event.key == K_w or event.key == K_s:
                    yrot_delta = 0
                elif event.key == K_e or event.key == K_d:
                    zrot_delta = 0
                elif event.key == K_LEFT or event.key == K_RIGHT:
                    xpos_delta = 0
                elif event.key == K_UP or event.key == K_DOWN:
                    zpos_delta = 0
                elif event.key == K_PAGEUP or event.key == K_PAGEDOWN:
                    ypos_delta = 0

if __name__ == '__main__':
    main()

