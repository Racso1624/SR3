#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#SR3

from gl import Render

r = Render()

r.glCreateWindow(1024, 1024)

r.glClearColor(0.5, 0.6, 0.8)

r.glColor(0, 0, 0)

r.glClear()

r.load('./cup.obj', translate=[512, 512], scale=[1, 1])

r.glFinish("sr3.bmp")