from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_TIMES_ROMAN_24


from ListaDeCoresRGB import *
from Poligonos import *

# **********************************************************************
# Imprime o texto S na posicao (x,y), com a cor 'cor'
# **********************************************************************
def PrintString(S: str, x: int, y: int, cor: tuple):
    defineCor(cor)
    glRasterPos3f(x, y, 0) # define posicao na tela

    for c in S:
        # GLUT_BITMAP_HELVETICA_10
        # GLUT_BITMAP_TIMES_ROMAN_24
        # GLUT_BITMAP_HELVETICA_18
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c))

def getBoundingByPoint(point: Ponto):
    bounding = Polygon()

    bounding.insereVertice(point.x-0.5, point.y-0.5, 0)
    bounding.insereVertice(point.x+0.5, point.y-0.5, 0)
    bounding.insereVertice(point.x+0.5, point.y+0.5, 0)
    bounding.insereVertice(point.x-0.5, point.y+0.5, 0)

    return bounding
