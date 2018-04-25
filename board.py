#!/usr/bin/env python3
import pygame.locals
import OpenGL.GLU
import OpenGL.GL
import numpy

class IdsBoard:
    def __init__(self, form, tiling, xdim,      ydim,      aspect,      fov_angle=70,   viewport_border=0.5,  rotatex=0,    rotatey=0,    dist=15,   transx=0,    transy=0,    lines=False, axis=False):
        self.form, self.tiling, self.xdim, self.ydim, self.aspect, self.fov_angle, self.viewport_border, self.rotatex, self.rotatey, self.dist, self.transx, self.transy, self.lines,  self.axis \
        =    form,      tiling,      xdim,      ydim,      aspect,      fov_angle,      viewport_border,      rotatex,      rotatey,      dist,      transx,      transy,      lines,       axis
        self.function_list = [self.flat,
                              self.cylinder, self.mobius,
                              self.torus,    self.klein,  self.real_proj_plane]
        self.window_width, self.window_height = pygame.display.get_surface().get_size()
        OpenGL.GL.glLineWidth(5.)

    def initialize_2D(self):
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
        OpenGL.GL.glPushMatrix()
        OpenGL.GL.glLoadIdentity()
        OpenGL.GL.glViewport(int(self.window_width*self.viewport_border), 0, int(self.window_width*(1-self.viewport_border)), self.window_height)
        OpenGL.GLU.gluOrtho2D(-1100, 1100, -1100, 1100)
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
        OpenGL.GL.glPushMatrix()
        OpenGL.GL.glLoadIdentity()
        OpenGL.GL.glShadeModel(OpenGL.GL.GL_FLAT)

    def initialize_3D(self, fov_angle, aspect, transx, transy, dist, rotatex, rotatey):
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
        OpenGL.GL.glPushMatrix()
        OpenGL.GL.glLoadIdentity()
        OpenGL.GL.glViewport(0,0,int(self.window_width*self.viewport_border), self.window_height)
        OpenGL.GLU.gluPerspective(fov_angle, aspect/2, 1, 50)
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
        OpenGL.GL.glPushMatrix()
        OpenGL.GL.glLoadIdentity()
        OpenGL.GL.glEnable(OpenGL.GL.GL_DEPTH_TEST)
        OpenGL.GL.glTranslatef(transx, transy, -dist) #The cube is drawn around the origin. Move the camera back a little.
        OpenGL.GL.glRotatef(rotatex, 1, 0, 0)
        OpenGL.GL.glRotatef(rotatey, 0, 1, 0)

    def pop(self):
        OpenGL.GL.glPopMatrix()
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
        OpenGL.GL.glPopMatrix()

    def draw_2D(self):
        self.initialize_2D()
        OpenGL.GL.glColor3fv((0.3, 0.3 , 0.3))
        OpenGL.GL.glBegin(OpenGL.GL.GL_QUADS)
        OpenGL.GL.glVertex3fv((-1100,-1100, -0.1))
        OpenGL.GL.glVertex3fv(( 1100,-1100, -0.1))
        OpenGL.GL.glVertex3fv(( 1100, 1100, -0.1))
        OpenGL.GL.glVertex3fv((-1100, 1100, -0.1))
        OpenGL.GL.glEnd()

        for x in range(self.xdim):
            OpenGL.GL.glBegin(OpenGL.GL.GL_QUAD_STRIP)
            OpenGL.GL.glVertex3fv((-1000+2000/self.xdim*x,     -1000, 0))
            OpenGL.GL.glVertex3fv((-1000+2000/self.xdim*(x+1), -1000, 0))
            for y in range(1,self.ydim+1):
                if (x+y)%2 == 0: OpenGL.GL.glColor3fv((0.2,0.1,0))
                else:            OpenGL.GL.glColor3fv((1,1,1))
                OpenGL.GL.glVertex3fv((-1000+2000/self.xdim*x,     -1000+2000/self.ydim*y, 0))
                OpenGL.GL.glVertex3fv((-1000+2000/self.xdim*(x+1), -1000+2000/self.ydim*y, 0))
            OpenGL.GL.glEnd()

        OpenGL.GL.glBegin(OpenGL.GL.GL_LINES)
        if self.form > 0:
            OpenGL.GL.glColor3fv((1,0,0))
            OpenGL.GL.glVertex3fv((-1000, -1000, 0.1))
            OpenGL.GL.glVertex3fv((-1000,  1000, 0.1))
            OpenGL.GL.glVertex3fv(( 1000, -1000, 0.1))
            OpenGL.GL.glVertex3fv(( 1000,  1000, 0.1))
            if self.form > 2:
                OpenGL.GL.glColor3fv((0,0,1))
                OpenGL.GL.glVertex3fv((-1000, -1000, 0.1))
                OpenGL.GL.glVertex3fv(( 1000, -1000, 0.1))
                OpenGL.GL.glVertex3fv((-1000,  1000, 0.1))
                OpenGL.GL.glVertex3fv(( 1000,  1000, 0.1))
        OpenGL.GL.glEnd()

        OpenGL.GL.glBegin(OpenGL.GL.GL_TRIANGLES)
        if self.form > 0:
            OpenGL.GL.glColor3fv((1,0,0))
            OpenGL.GL.glVertex3fv((-1000-50, -1000+2000/3-50, 0.1))
            OpenGL.GL.glVertex3fv((-1000+50, -1000+2000/3-50, 0.1))
            OpenGL.GL.glVertex3fv((-1000,    -1000+2000/3+50, 0.1))
            OpenGL.GL.glVertex3fv((-1000-50, -1000+4000/3-50, 0.1))
            OpenGL.GL.glVertex3fv((-1000+50, -1000+4000/3-50, 0.1))
            OpenGL.GL.glVertex3fv((-1000,    -1000+4000/3+50, 0.1))
            if self.form in [1, 3, 4]: i = -50 #cylinder, torus or Klein bottle
            else: i = 50
            OpenGL.GL.glVertex3fv(( 1000-50, -1000+2000/3+i, 0.1))
            OpenGL.GL.glVertex3fv(( 1000+50, -1000+2000/3+i, 0.1))
            OpenGL.GL.glVertex3fv(( 1000,    -1000+2000/3-i, 0.1))
            OpenGL.GL.glVertex3fv(( 1000-50, -1000+4000/3+i, 0.1))
            OpenGL.GL.glVertex3fv(( 1000+50, -1000+4000/3+i, 0.1))
            OpenGL.GL.glVertex3fv(( 1000,    -1000+4000/3-i, 0.1))
            if self.form > 2:
                OpenGL.GL.glColor3fv((0,0,1))
                OpenGL.GL.glVertex3fv((-1000+2000/3-50, -1000+50, 0.1))
                OpenGL.GL.glVertex3fv((-1000+2000/3-50, -1000-50, 0.1))
                OpenGL.GL.glVertex3fv((-1000+2000/3+50, -1000,    0.1))
                OpenGL.GL.glVertex3fv((-1000+4000/3-50, -1000+50, 0.1))
                OpenGL.GL.glVertex3fv((-1000+4000/3-50, -1000-50, 0.1))
                OpenGL.GL.glVertex3fv((-1000+4000/3+50, -1000,    0.1))
                if self.form == 3 : i = -50
                else: i = 50
                OpenGL.GL.glVertex3fv((-1000+2000/3+i, 1000+50, 0.1))
                OpenGL.GL.glVertex3fv((-1000+2000/3+i, 1000-50, 0.1))
                OpenGL.GL.glVertex3fv((-1000+2000/3-i, 1000,    0.1))
                OpenGL.GL.glVertex3fv((-1000+4000/3+i, 1000+50, 0.1))
                OpenGL.GL.glVertex3fv((-1000+4000/3+i, 1000-50, 0.1))
                OpenGL.GL.glVertex3fv((-1000+4000/3-i, 1000,    0.1))
        OpenGL.GL.glEnd()
        self.pop()

    def draw_3D(self):
        self.initialize_3D(self.fov_angle, self.aspect, self.transx, self.transy, self.dist, self.rotatex, self.rotatey)
        self.function_list[self.form](self.xdim, self.ydim)
        if self.lines: self.draw_lines(self.form)
        if self.axis:  self.draw_axis()
        self.pop()

    def flat(self, xdim, ydim):
        OpenGL.GL.glDisable(OpenGL.GL.GL_CULL_FACE)
        OpenGL.GL.glBegin(OpenGL.GL.GL_QUADS)
        for i, x in enumerate(numpy.arange(-xdim/2, xdim/2, 1)):
            for j, y in enumerate(numpy.arange(-ydim/2, ydim/2, 1)):
                if (i+j)%2 == 0: OpenGL.GL.glColor3fv((0.2,0.1,0))
                else:            OpenGL.GL.glColor3fv((1,1,1))
                OpenGL.GL.glVertex3fv((x, y, 0))
                OpenGL.GL.glVertex3fv((x+1, y, 0))
                OpenGL.GL.glVertex3fv((x+1, y+1, 0))
                OpenGL.GL.glVertex3fv((x, y+1, 0))
        OpenGL.GL.glEnd()

    def cylinder(self, xdim, ydim):
        OpenGL.GL.glDisable(OpenGL.GL.GL_CULL_FACE)
        OpenGL.GL.glShadeModel(OpenGL.GL.GL_FLAT) #No interpolation of colors while drawing GL_QUAD_STRIP
        radius = 1/(2*numpy.tan(numpy.pi/xdim))
        for x in range(xdim):
            OpenGL.GL.glBegin(OpenGL.GL.GL_QUAD_STRIP)
            OpenGL.GL.glVertex3fv((radius, -ydim/2, 0.5))
            OpenGL.GL.glVertex3fv((radius, -ydim/2, -0.5))
            for i, y in enumerate(numpy.arange(-ydim/2, ydim/2, 1)):
                if (x+i)%2 == 0: OpenGL.GL.glColor3fv((0.2,0.1,0))
                else:            OpenGL.GL.glColor3fv((1,1,1))
                OpenGL.GL.glVertex3fv((radius, y+1, 0.5))
                OpenGL.GL.glVertex3fv((radius, y+1, -0.5))
            OpenGL.GL.glEnd()
            OpenGL.GL.glRotatef(360/xdim,0,1,0)

    def mobius(self, xdim, ydim):
        OpenGL.GL.glShadeModel(OpenGL.GL.GL_FLAT) #No interpolation of colors while drawing GL_QUAD_STRIP
        radius = 2/(2*numpy.tan(numpy.pi/xdim))
        r2 = radius-0.25
        angle = numpy.pi/xdim
        for x in range(xdim):
            OpenGL.GL.glBegin(OpenGL.GL.GL_QUAD_STRIP)
            for i,y in enumerate(numpy.arange(-1,1+1./ydim,2./ydim)):
                if (x+i)%2 == 0: OpenGL.GL.glColor3fv((0.2,0.1,0))
                else:            OpenGL.GL.glColor3fv((1,1,1))
                OpenGL.GL.glVertex3fv((  numpy.cos(2*angle*x)*(radius+y*numpy.cos(angle*x)*r2),
                                         y*r2*numpy.sin(angle*x),
                                         numpy.sin(2*angle*x)*(radius+y*r2*numpy.cos(angle*x))))
                OpenGL.GL.glVertex3fv((  numpy.cos(2*angle*(x+1))*(radius+y*numpy.cos(angle*(x+1))*r2),
                                         y*r2*numpy.sin(angle*(x+1)),
                                         numpy.sin(2*angle*(x+1))*(radius+y*r2*numpy.cos(angle*(x+1)))))
            OpenGL.GL.glEnd()

    def torus(self, xdim, ydim):
        OpenGL.GL.glEnable(OpenGL.GL.GL_CULL_FACE); #Only draw one side of the objects
        OpenGL.GL.glCullFace(OpenGL.GL.GL_BACK); #Only draw the part that faces the camera.
        apothema = 1/(2*numpy.tan(numpy.pi/xdim))
        major_radius = 2*apothema
        OpenGL.GL.glTranslatef(major_radius,0,0)
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
        OpenGL.GL.glTranslatef(-major_radius,0,0)

    def klein(self, xdim, ydim):
        w=xdim/4
        h=8/3*w
        r=2/(2*numpy.tan(numpy.pi/ydim))
        xstep = 2*numpy.pi/xdim
        OpenGL.GL.glShadeModel(OpenGL.GL.GL_FLAT)
        OpenGL.GL.glDisable(OpenGL.GL.GL_CULL_FACE)
        for i, x in enumerate(numpy.arange(0, 2*numpy.pi-numpy.pi/xdim, 2*numpy.pi/xdim)):
            if (i+1)/xdim>0.75:
                OpenGL.GL.glDisable(OpenGL.GL.GL_CULL_FACE)
            elif (i+1)/xdim>0.3:
                OpenGL.GL.glEnable(OpenGL.GL.GL_CULL_FACE)
                OpenGL.GL.glCullFace(OpenGL.GL.GL_BACK)
            OpenGL.GL.glBegin(OpenGL.GL.GL_QUAD_STRIP)
            for j, y in enumerate(numpy.arange(0, 2*numpy.pi+numpy.pi/ydim, 2*numpy.pi/ydim)):
                if (i+j)%2 == 0: OpenGL.GL.glColor3fv((0.2,0.1,0))
                else:            OpenGL.GL.glColor3fv((1,1,1))
                OpenGL.GL.glVertex3fv((w*numpy.cos(x)*(1+numpy.sin(x))
                                      +r*(1-0.5*numpy.cos(x))*numpy.cos(x*(x<=numpy.pi))*numpy.cos(y+numpy.pi*(x>numpy.pi)),
                                       h*numpy.sin(x)
                                      +r*(1-0.5*numpy.cos(x))*numpy.sin(x)*numpy.cos(y)*(x<numpy.pi),
                                       r*(1-0.5*numpy.cos(x))*numpy.sin(y)))
                OpenGL.GL.glVertex3fv((w*numpy.cos(x+xstep)*(1+numpy.sin(x+xstep))
                                      +r*(1-0.5*numpy.cos(x+xstep))*numpy.cos((x+xstep)*(x+xstep<=numpy.pi))*numpy.cos(y+numpy.pi*(x+xstep>numpy.pi)),
                                       h*numpy.sin(x+xstep)
                                      +r*(1-0.5*numpy.cos(x+xstep))*numpy.sin(x+xstep)*numpy.cos(y)*(x+xstep<=numpy.pi),
                                       r*(1-0.5*numpy.cos(x+xstep))*numpy.sin(y)))
            OpenGL.GL.glEnd()

    def real_proj_plane(self, xdim, ydim):
        OpenGL.GL.glDisable(OpenGL.GL.GL_CULL_FACE); #Only draw one side of the objects
        OpenGL.GL.glShadeModel(OpenGL.GL.GL_FLAT)
        xstep = 2*numpy.pi/xdim
        r=2
        for i, x in enumerate(numpy.arange(0, 2*numpy.pi-numpy.pi/xdim, 2*numpy.pi/xdim)):
            OpenGL.GL.glBegin(OpenGL.GL.GL_QUAD_STRIP)
            for j, y in enumerate(numpy.arange(0, 2*numpy.pi+numpy.pi/ydim, 2*numpy.pi/ydim)):
                if (i+j)%2 == 0: OpenGL.GL.glColor3fv((0.2,0.1,0))
                else:            OpenGL.GL.glColor3fv((1,1,1))
                OpenGL.GL.glVertex3fv((r*(1+numpy.cos(y))*numpy.cos(x),
                                       r*(1+numpy.cos(y))*numpy.sin(x),
                                      -numpy.tanh(x-numpy.pi)*r*numpy.sin(y)))
                OpenGL.GL.glVertex3fv((r*(1+numpy.cos(y))*numpy.cos(x+xstep),
                                       r*(1+numpy.cos(y))*numpy.sin(x+xstep),
                                      -numpy.tanh(x+xstep-numpy.pi)*r*numpy.sin(y)))
            OpenGL.GL.glEnd()

    def draw_lines(self):
        return

    def draw_axis(self, radius, color):
        OpenGL.GL.glColor3fv(color)
        OpenGL.GL.glBegin(OpenGL.GL.GL_LINES)
        OpenGL.GL.glVertex3fv((0,      0,      0))
        OpenGL.GL.glVertex3fv((radius, 0,      0))
        OpenGL.GL.glVertex3fv((0,      0,      0))
        OpenGL.GL.glVertex3fv((0,      radius, 0))
        OpenGL.GL.glVertex3fv((0,      0,      0))
        OpenGL.GL.glVertex3fv((0,      0,      radius))
        OpenGL.GL.glEnd()

class KeyListener:
    def __init__(self, board):
        self.board = board
        self.trans_x_speed, self.rot_x_speed, self.rot_y_speed, self.trans_z_speed, self.viewport_speed \
        =    0,                  0,                0,                0,                  0
        return

    def __call__(self):
        for event in pygame.event.get(): #This is getting the basic listeners
            if event.type == pygame.QUIT: #What to do if the close button is pressed
                pygame.quit() #Stop the game!
                quit() #Stop the python!

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.board.dist += 0.06
                if event.button == 5:
                    self.board.dist -= 0.06

            if (event.type == pygame.MOUSEMOTION) and (event.buttons[0] == 1):
                print(event)
                self.board.rotatex += event.rel[1]*0.5
                self.board.rotatey += event.rel[0]*0.5

            if (event.type == pygame.KEYDOWN):
                print(event)
                if event.key == 113: #q
                    self.viewport_speed += -1
                if event.key == 101: #e
                    self.viewport_speed += 1
                if event.key == 97: #a
                    self.trans_x_speed += 1
                if event.key == 100: #d
                    self.trans_x_speed += -1
                if event.key == 115: #s
                    self.trans_z_speed += -1
                if event.key == 119: #w
                    self.trans_z_speed += 1
                if event.key == 273: #up
                    self.rot_x_speed += 1
                if event.key == 274: #down
                    self.rot_x_speed += -1
                if event.key == 275: #left
                    self.rot_y_speed += -1
                if event.key == 276: #right
                    self.rot_y_speed += 1

            if (event.type == pygame.KEYUP):
                if event.key == 113: #q
                    self.viewport_speed += 1
                if event.key == 101: #e
                    self.viewport_speed += -1
                if event.key == 97: #a
                    self.trans_x_speed += -1
                if event.key == 100: #d
                    self.trans_x_speed += 1
                if event.key == 115: #s
                    self.trans_z_speed += 1
                if event.key == 119: #w
                    self.trans_z_speed += -1
                if event.key == 273:
                    self.rot_x_speed += -1
                if event.key == 274:
                    self.rot_x_speed += 1
                if event.key == 275:
                    self.rot_y_speed += 1
                if event.key == 276:
                    self.rot_y_speed += -1

        self.board.rotatex          += 2*self.rot_x_speed
        self.board.rotatey          += 2*self.rot_y_speed
        self.board.transx           += 0.25*self.trans_x_speed
        self.board.dist             += 0.03*self.trans_z_speed
        self.board.viewport_border  += 0.01*self.viewport_speed

def main():
    pygame.init()
    rotatex, rotatey, dist, transx, transy, angle = 0, 0, -15., 0, 0, 70
    display = (1800,900) #Tiniest screen resolution as window size.
    pygame.display.set_mode(display, pygame.locals.DOUBLEBUF|pygame.OPENGL)
    aspect = (display[0]/display[1])

    board = IdsBoard(4, 4, 13, 8, aspect)
    listener = KeyListener(board)

    while True:
        listener()
        OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT|OpenGL.GL.GL_DEPTH_BUFFER_BIT) #Make sure it doesn't draw anything where there's not supposed to be anything. Remove it for sticky pixels.
        board.draw_3D()
        board.draw_2D()
        pygame.display.flip() #Updates the display with new contents.
        pygame.time.wait(10) #Wait 10 miliseconds per frame for a 100fps.

        # #Je moeder
        # font = pygame.font.Font (None, 64)
        # textSurface = font.render("2D radius: "+str(flatwidth), False, (255,255,255,128), (0,0,0,0))
        # textData = pygame.image.tostring(textSurface, "RGBA", True)
        # OpenGL.GL.glEnable(OpenGL.GL.GL_BLEND)
        # OpenGL.GL.glBlendFunc(OpenGL.GL.GL_ONE, OpenGL.GL.GL_SRC_ALPHA)
        # OpenGL.GL.glRasterPos3d(-2.75,-2.0625,0)
        # OpenGL.GL.glDrawPixels(textSurface.get_width(), textSurface.get_height(), OpenGL.GL.GL_RGBA, OpenGL.GL.GL_UNSIGNED_BYTE, textData)
        # OpenGL.GL.glDisable(OpenGL.GL.GL_BLEND)

main() #Kinda java style.. Runs above code.