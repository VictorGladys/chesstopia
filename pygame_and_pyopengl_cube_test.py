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

def Cube(rotatex, rotatey, dist):
    """Define the basic parts of a 2x2x2 cube"""
    corners= (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
        )

    edges = (
        (0,1),
        (0,3),
        (0,4),
        (2,1),
        (2,3),
        (2,7),
        (6,3),
        (6,4),
        (6,7),
        (5,1),
        (5,4),
        (5,7)
        )

    faces = (
        (0,1,2,3),
        (3,2,7,6),
        (6,7,5,4),
        (4,5,1,0),
        (1,5,7,2),
        (4,0,3,6)
        )

    colors = [  (1,0,0),
        (0,1,0),
        (0,0,1),
        (1,1,0),
        (1,0,1),
        (0,1,1)] #To easily switch colors between drawing faces.

    OpenGL.GL.glLineWidth(5.)
    """
    There is about 0 configuration you can do in between glBegin and glEnd.
    If you want to define the line width of your edges, or the culling of your faces... do it before glBegin.
    This also means it is a big PITA to get just one of the edges to be more broad. You'll have to start two instances of GL_LINES.
    """
    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
    OpenGL.GL.glPushMatrix()
    OpenGL.GL.glLoadIdentity()
    OpenGL.GLU.gluPerspective(45, (800 / 600), 1, 10)
    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
    OpenGL.GL.glPushMatrix()
    OpenGL.GL.glLoadIdentity()
    OpenGL.GL.glTranslatef(0.0,0.0, dist) #The cube is drawn around the origin. Move the camera back a little.
    OpenGL.GL.glRotatef(rotatex, 1, 0, 0)
    OpenGL.GL.glRotatef(rotatey, 0, 1, 0) #Rotate every frame. The first value is the angle which is rotated (read: rotation speed), values 2-4 give a 3D vector / axis to rotate about.
    OpenGL.GL.glBegin(OpenGL.GL.GL_LINES) #You'll have to define what kind of object you are drawing. Polygons? Quadrilaterals? Lines? They all start their own drawing instance it seems.
    OpenGL.GL.glColor3fv((1,1,1)) #This is an exception! You can define color in between glBegin and glEnd!
    for edge in edges:
        for vertex in edge:
            OpenGL.GL.glVertex3fv(corners[vertex]) #Draws a line (we're in GL_LINES mode) in between the two 3D-tuples that are called in separate instances of this function. e.g. You'll have to call this function at least twice to draw something.
    OpenGL.GL.glEnd()


    OpenGL.GL.glCullFace(OpenGL.GL.GL_FRONT); #Only draw the part that faces the camera.
    OpenGL.GL.glEnable(OpenGL.GL.GL_CULL_FACE); #Only draw part of the objects
    OpenGL.GL.glBegin(OpenGL.GL.GL_QUADS)
    i=0
    for surface in faces:
        OpenGL.GL.glColor3fv(colors[i])
        i+=1 #swap colors.
        for vertex in surface:
            OpenGL.GL.glVertex3fv(corners[vertex]) #Will only draw one quadrilateral every 4 times you call this function with a tuple in 3D space.
    OpenGL.GL.glEnd()
    OpenGL.GL.glPopMatrix()
    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
    OpenGL.GL.glPopMatrix()

def main():
    pygame.init()
    rotatex, rotatey, dist = 0, 0, -5.
    display = (800,600) #Tiniest screen resolution as window size.
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
    OpenGL.GLU.gluPerspective(45, (display[0]/display[1]), 1, 20)

    OpenGL.GL.glTranslatef(0.0,0.0, -5) #The cube is drawn around the origin. Move the camera back a little.

    # pygame.key.set_repeat(1,10)
    xspeed, yspeed, radspeed = 0, 0, 0

    while True:
        for event in pygame.event.get(): #This is getting the basic listeners.
            if event.type == pygame.QUIT: #What to do if the close button is pressed
                pygame.quit() #Stop the game!
                quit() #Stop the python!
            if (event.type == pygame.MOUSEMOTION) and (event.buttons[0] == 1):
                print(event)
                OpenGL.GL.glRotatef(event.rel[0], 0, 1, 0)
                OpenGL.GL.glRotatef(event.rel[1], 1, 0, 0)
            if (event.type == pygame.KEYDOWN):
                if event.key == 115: #s
                    radspeed += -1
                if event.key == 119: #w
                    radspeed += 1
                if event.key == 273:
                    xspeed += 1
                if event.key == 274:
                    xspeed += -1
                if event.key == 275:
                    yspeed += -1
                if event.key == 276:
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
        # print(pygame.mouse.get_pressed())
        rotatex += xspeed
        rotatey += yspeed
        dist += 0.03*radspeed

        # print(OpenGL.GL.glGetFloatv())
        OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT|OpenGL.GL.GL_DEPTH_BUFFER_BIT) #Make sure it doesn't draw anything where there's not supposed to be anything. Remove it for sticky pixels.
        Cube(rotatex, rotatey, dist) #Actually draw the fucking cube. Is defined above.
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