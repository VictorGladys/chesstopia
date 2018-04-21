#!/usr/bin/env python3
"""
Seriously, what?
import pygame < Not recursive.
import OpenGL < Same problem.

pygame has very good documentation at pygame.org.
For OpenGL... good luck! Most demos and tutorials are written for python2 and riddled with bugs, not to mention many years old.
"""
import pygame.locals
import OpenGL.GLU
import OpenGL.GL
import numpy
def DrawBoard(tiling, form, xdim, ydim, aspect, rotatex, rotatey, dist, transx, transy, lines):
    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
    OpenGL.GL.glPushMatrix()
    OpenGL.GL.glLoadIdentity()
    OpenGL.GLU.gluPerspective(45, aspect, 1, 30)
    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
    OpenGL.GL.glPushMatrix()
    OpenGL.GL.glLoadIdentity()
    OpenGL.GL.glCullFace(OpenGL.GL.GL_BACK); #Only draw the part that faces the camera.
    OpenGL.GL.glEnable(OpenGL.GL.GL_CULL_FACE); #Only draw part of the objects
    OpenGL.GL.glTranslatef(transx, transy, dist) #The cube is drawn around the origin. Move the camera back a little.
    OpenGL.GL.glRotatef(rotatex, 1, 0, 0)
    OpenGL.GL.glRotatef(rotatey, 0, 1, 0) #Rotate every frame. The first value is the angle which is rotated (read: rotation speed), values 2-4 give a 3D vector / axis to rotate about.
    if lines:
        OpenGL.GL.glColor3fv((1,1,1))
        OpenGL.GL.glLineWidth(5.)
        OpenGL.GL.glBegin(OpenGL.GL.GL_LINES)
        OpenGL.GL.glVertex3fv((-xdim/2, -ydim/2, 0))
        OpenGL.GL.glVertex3fv((xdim/2, -ydim/2, 0))
        OpenGL.GL.glVertex3fv((xdim/2, -ydim/2, 0))
        OpenGL.GL.glVertex3fv((xdim/2, ydim/2, 0))
        OpenGL.GL.glVertex3fv((xdim/2, ydim/2, 0))
        OpenGL.GL.glVertex3fv((-xdim/2, ydim/2, 0))
        OpenGL.GL.glVertex3fv((-xdim/2, ydim/2, 0))
        OpenGL.GL.glVertex3fv((-xdim/2, -ydim/2, 0))
        OpenGL.GL.glEnd()

    if form == 0: #Flat surface
        OpenGL.GL.glDisable(OpenGL.GL.GL_CULL_FACE)
        OpenGL.GL.glBegin(OpenGL.GL.GL_QUADS)
        for x in numpy.arange(-xdim/2, xdim/2, 1):
            for y in numpy.arange(-ydim/2, ydim/2, 1):
                if (x+y)%2 == 0: OpenGL.GL.glColor3fv((0.2,0.1,0))
                else:            OpenGL.GL.glColor3fv((1,1,1))
                OpenGL.GL.glVertex3fv((x, y, 0))
                OpenGL.GL.glVertex3fv((x+1, y, 0))
                OpenGL.GL.glVertex3fv((x+1, y+1, 0))
                OpenGL.GL.glVertex3fv((x, y+1, 0))
        OpenGL.GL.glEnd()
    elif form == 1: #cylinder
        OpenGL.GL.glShadeModel(OpenGL.GL.GL_FLAT)
        radius = 1/(2*numpy.tan(numpy.pi/xdim))
        for x in range(xdim):
            OpenGL.GL.glBegin(OpenGL.GL.GL_QUAD_STRIP)
            OpenGL.GL.glVertex3fv((radius, -ydim/2, 0.5))
            OpenGL.GL.glVertex3fv((radius, -ydim/2, -0.5))
            for y in numpy.arange(-ydim/2, ydim/2, 1):
                if (x+y)%2 == 0: OpenGL.GL.glColor3fv((0.2,0.1,0))
                else:            OpenGL.GL.glColor3fv((1,1,1))
                OpenGL.GL.glVertex3fv((radius, y+1, 0.5))
                OpenGL.GL.glVertex3fv((radius, y+1, -0.5))
            OpenGL.GL.glEnd()
            OpenGL.GL.glRotatef(360/xdim,0,1,0)
    elif form == 2: #cylinder
        OpenGL.GL.glCullFace(OpenGL.GL.GL_BACK); #Only draw the part that faces the camera.
        apothema = 1/(2*numpy.tan(numpy.pi/xdim))
        major_radius = 2*apothema
        OpenGL.GL.glTranslatef(major_radius,0,0)
        # print(major_radius, apothema, major_radius-apothema, major_radius+apothema)
        for y in range(ydim):
            for x in range(xdim):
                OpenGL.GL.glRotatef(360/xdim,0,0,1)
                OpenGL.GL.glBegin(OpenGL.GL.GL_QUADS)
                if (y+x)%2 == 0: OpenGL.GL.glColor3fv((0.2,0.1,0))
                else:            OpenGL.GL.glColor3fv((1,1,1))
                z1 = (1-0.5/numpy.cos(numpy.pi/xdim)*numpy.cos((x+1.5)*2*numpy.pi/xdim))*numpy.tan(numpy.pi/ydim)/numpy.tan(numpy.pi/xdim)
                z2 =(1-0.5/numpy.cos(numpy.pi/xdim)*numpy.cos((x+0.5)*2*numpy.pi/xdim))*numpy.tan(numpy.pi/ydim)/numpy.tan(numpy.pi/xdim)
                OpenGL.GL.glVertex3fv((-apothema, -0.5, -z1))
                OpenGL.GL.glVertex3fv((-apothema, -0.5, z1))
                OpenGL.GL.glVertex3fv((-apothema, 0.5, z2))
                OpenGL.GL.glVertex3fv((-apothema, 0.5, -z2))
                OpenGL.GL.glEnd()
            OpenGL.GL.glTranslatef(-major_radius,0,0)
            OpenGL.GL.glRotatef(360/ydim,0,1,0)
            OpenGL.GL.glTranslatef(major_radius,0,0)
    OpenGL.GL.glPopMatrix()
    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
    OpenGL.GL.glPopMatrix()

def main():
    pygame.init()
    rotatex, rotatey, dist, transx, transy = 0, 0, -15., 0, 0
    display = (1800,1000) #Tiniest screen resolution as window size.
    """
    So, what do the next function calls do?

    pygame.display.set_mode initializes a window for display.
    It takes 1-3 values:    Resolution is a 2D tuple with the resolution you want.
                            Flags are a few flags, don't know how they work, you can add them together.
                                pygame.OPENGL is necessary to get an actual display of our openGL graphics going on, however,
                                pygame.DOUBLEBUF is 'recommended for OpenGL' according to pygame.org,
                                pygame.FULLSCREEN forces fullscreen. Note that the display resolution is still in place! The rest is just filled with background.
                                    ^-It seems to be difficult to exit this mode.. Can be solved with pygame events later on.
                            Depth is the amount of bits you want to use for color. Leaving it out usually results in the optimal color depth for your system.

    openGL.GLU.gluPerspective defines the camera,
    and takes four values:  Field of view angle, 0 gives 0 perspective (tunnel vision), 45 is quite standard, 360 is full view.
                            Aspect ratio, just take width/height to transform correctly.
                            zNear, anything that is closer than this to the camera won't be drawn, so better take a small value.
                            zFar, anything that is farther than this to the camera won't be drawn, so better take a large value.
    """
    pygame.display.set_mode(display, pygame.locals.DOUBLEBUF|pygame.OPENGL)
    aspect = (display[0]/display[1])
    OpenGL.GLU.gluPerspective(45, aspect, 1, 20)
    OpenGL.GL.glTranslatef(0.0,0.0, -5) #The cube is drawn around the origin. Move the camera back a little.
    # pygame.key.set_repeat(1,10)
    xspeed, yspeed, radspeed = 0, 0, 0

    while True:
        for event in pygame.event.get(): #This is getting the basic listeners.
            if event.type == pygame.QUIT: #What to do if the close button is pressed
                pygame.quit() #Stop the game!
                quit() #Stop the python!
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    dist += 0.06
                if event.button == 5:
                    dist -= 0.06
            if (event.type == pygame.MOUSEMOTION) and (event.buttons[0] == 1):
                print(event)
                rotatex += event.rel[1]*0.5
                rotatey += event.rel[0]*0.5
            if (event.type == pygame.KEYDOWN):
                if event.key == 115: #s
                    radspeed += -1
                if event.key == 119: #w
                    radspeed += 1
                if event.key == 273: #up
                    xspeed += 1
                if event.key == 274: #down
                    xspeed += -1
                if event.key == 275: #left
                    yspeed += -1
                if event.key == 276: #right
                    yspeed += 1
                print(event)
            if (event.type == pygame.KEYUP):
                if event.key == 115: #s
                    radspeed += 1
                if event.key == 119: #w
                    radspeed += -1
                if event.key == 273:
                    xspeed += -1
                if event.key == 274:
                    xspeed += 1
                if event.key == 275:
                    yspeed += 1
                if event.key == 276:
                    yspeed += -1

        rotatex += 2*xspeed
        rotatey += 2*yspeed
        dist += 0.03*radspeed

        OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT|OpenGL.GL.GL_DEPTH_BUFFER_BIT) #Make sure it doesn't draw anything where there's not supposed to be anything. Remove it for sticky pixels.

        DrawBoard(4, 2, 20, 8, aspect, rotatex, rotatey, dist, transx, transy, False)


        font = pygame.font.Font (None, 64)
        textSurface = font.render("Je moeder", False, (255,255,255,128), (0,0,0,0))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        # print(textData)
        OpenGL.GL.glEnable(OpenGL.GL.GL_BLEND)
        OpenGL.GL.glBlendFunc(OpenGL.GL.GL_ONE, OpenGL.GL.GL_SRC_ALPHA)
        OpenGL.GL.glRasterPos3d(-2.75,-2.0625,0)
        OpenGL.GL.glDrawPixels(textSurface.get_width(), textSurface.get_height(), OpenGL.GL.GL_RGBA, OpenGL.GL.GL_UNSIGNED_BYTE, textData)
        OpenGL.GL.glDisable(OpenGL.GL.GL_BLEND)
        pygame.display.flip() #Updates the display with new contents.
        pygame.time.wait(10) #Wait 10 miliseconds per frame for a 100fps.

main() #Kinda java style.. Runs above code.





