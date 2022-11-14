#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#SR3

import struct
from obj import *

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(h):
    #2 bytes
    return struct.pack('=h', h)

def dword(l):
    #4 bytes
    return struct.pack('=l', l)

def setColor(r, b, g):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

class Render(object):

    def __init__(self):
        self.width = 0
        self.height = 0
        self.clear_color = setColor(1, 1, 1)
        self.render_color = setColor(0, 0, 0)
        self.viewport_color = setColor(1, 1, 1)
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_height = 0
        self.viewport_width = 0

    def glClear(self):
        self.framebuffer = [[self.clear_color for x in range(self.width)]
        for y in range(self.height)]

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewportColor(self, r, g, b):
        self.viewport_color = setColor(r, g, b)

    def glClearColor(self, r, g, b):
        self.clear_color = setColor(r, g, b)

    def glClearViewport(self):
        for x in range(self.viewport_x, self.viewport_x + self.viewport_width + 1):
            for y in range(self.viewport_y, self.viewport_y + self.viewport_height + 1):
                self.glPoint(x,y, self.viewport_color)    
        

    def glColor(self, r, g, b):
        self.render_color = setColor(r, g, b)

    def glViewPort(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def glVertex(self, x, y):
        if x > 1 or x < -1 or y > 1 or y < -1:
            print('Error')
        else:
            x = int((x + 1) * (self.viewport_width / 2) + self.viewport_x)
            y = int((y + 1) * (self.viewport_height / 2) + self.viewport_y)

            self.glPoint(x, y)

    def glPoint(self, x, y, color = None):
        self.framebuffer[x][y] = color or self.render_color

    def glLine(self, x0, x1, y0, y1, color = None):
        
        line_color = color or self.render_color

        if x0 == x1:
            if y0 == y1:
                self.glPoint(x0, y0, line_color)
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0

        threshold = dx

        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(x, y, line_color)
            else:
                self.glPoint(y, x, line_color)

            offset += dy * 2
            
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += dx * 2

    def load(self, filename, translate, scale):
        model = Obj(filename)


        for face in model.faces:
            vcount = len(face)
            
            for j in range(vcount):
                vi1 = face[j][0] 
                vi2 = face[(j + 1) % vcount][0]

                v1 = model.vertices[vi1 - 1]
                v2 = model.vertices[vi2 - 1]

                #print(v1, v2)

                x1 = round((v1[0] + translate[0]) * scale[0])
                x2 = round((v1[1] + translate[1]) * scale[1])
                y1 = round((v2[0] + translate[0]) * scale[0])
                y2 = round((v2[1] + translate[1]) * scale[1])

                #print(x1, x2, y1, y2)

                self.glLine(x1, x2, y1, y2)


    def glFinish(self, filename):
        f = open(filename, 'bw')

        #pixel header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        #info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #pixel data
        for x in range (self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])

        f.close()