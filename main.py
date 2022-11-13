#Oscar Fernando López Barrios
#Carné 20679
#Gráficas Por Computadora
#SR3

from gl import Render

r = Render()

r.glCreateWindow(1000, 1000)

r.glClearColor(0.2, 0.4, 0.6)

r.glClear()

r.glFinish("sr3.bmp")