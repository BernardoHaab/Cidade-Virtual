# ***********************************************************************************
#   OpenGLBasico3D-V5.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe dois Cubos em OpenGL
#   Para maiores informações, consulte
#
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Outro exemplo de código em Python, usando OpenGL3D pode ser obtido em
#   http://openglsamples.sourceforge.net/cube_py.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
#
# ***********************************************************************************
#from PIL import Image
import math
import time
from random import randrange

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

from Linha import Linha
from Ponto import Ponto

Angulo = 0.0

alvoObs = Ponto(0, 0, 9)
posicaoObs = Ponto(0, 5, 10)

posCarro = Ponto(0, 0, 0)
dirCarro = Ponto(0, 0, 1)

anguloRotacao = 5
anguloSomatorio = 0
velCarro = 0.25

moving = False

mapa = []
tamMapaZ = 0
tamMapaX = 0
texturas = []

pontoGas = Ponto(0,0,0)
mapaGas = (0,0)
gasTotal = 100

primeiraPessoa = True

# **********************************************************************
#  init()
#  Inicializa os parÃ¢metros globais de OpenGL
#/ **********************************************************************
def init():
    global mapa
    # Define a cor do fundo da tela (BRANCO)
    glClearColor(0.5, 0.5, 0.5, 1.0)

    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable (GL_CULL_FACE )
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    texturas.append(loadTexture("texturas/CROSS.jpg"))
    texturas.append(loadTexture("texturas/DL.jpg"))
    texturas.append(loadTexture("texturas/DLR.jpg"))
    texturas.append(loadTexture("texturas/DR.jpg"))
    texturas.append(loadTexture("texturas/LR.jpg"))
    texturas.append(loadTexture("texturas/None.jpg"))
    texturas.append(loadTexture("texturas/UD.jpg"))
    texturas.append(loadTexture("texturas/UDL.jpg"))
    texturas.append(loadTexture("texturas/UDR.jpg"))
    texturas.append(loadTexture("texturas/UL.jpg"))
    texturas.append(loadTexture("texturas/ULR.jpg"))
    texturas.append(loadTexture("texturas/UR.jpg"))

    carregaGasolina()

def carregaGasolina():
    global pontoGas, mapaGas
    conversorZ = 60 / tamMapaZ
    conversorX = 60 / tamMapaX

    novoX = randrange(0, 30)
    novoZ = randrange(0, 30)

    while mapa[novoZ][novoX] <= 0 or mapa[novoZ][novoX] > 13:
        novoX = randrange(0, 30)
        novoZ = randrange(0, 30)

    print("novoX:", novoX)
    print("novoX*conversorX:", novoX*conversorX)
    print("novoZ:", novoZ)
    print("Linha: ", tamMapaZ - novoZ-1)
    print("Coluna: ", tamMapaX - novoX-1)
    print("novoZ*conversorZ:", novoZ*conversorZ)
    print("Ponto Mapa:", mapa[novoZ][novoX])

    mapaGas = (tamMapaX - novoX - 1, tamMapaZ - novoZ - 1)
    pontoGas = Ponto(mapaGas[0]*conversorX, 0, mapaGas[1]*conversorZ )
    pontoGas.imprime('Posic Gas')


# **********************************************************************
# LoadTexture
# Retorna o id da textura lida
# **********************************************************************
def loadTexture(nome) -> int:
    # carrega a imagem
    image = Image.open(nome)
    # print ("X:", image.size[0])
    # print ("Y:", image.size[1])
    # converte para o formato de OpenGL
    img_data = np.array(list(image.getdata()), np.uint8)

    # Habilita o uso de textura
    glEnable ( GL_TEXTURE_2D )

    #Cria um ID para texura
    texture = glGenTextures(1)
    errorCode =  glGetError()
    if errorCode == GL_INVALID_OPERATION:
        print ("Erro: glGenTextures chamada entre glBegin/glEnd.")
        return -1

    # Define a forma de armazenamento dos pixels na textura (1= alihamento por byte)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # Define que tipo de textura ser usada
    # GL_TEXTURE_2D ==> define que ser· usada uma textura 2D (bitmaps)
    # e o nro dela
    glBindTexture(GL_TEXTURE_2D, texture)

    # texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    errorCode = glGetError()
    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    # neste ponto, "texture" tem o nro da textura que foi carregada
    errorCode = glGetError()
    if errorCode == GL_INVALID_OPERATION:
        print ("Erro: glTexImage2D chamada entre glBegin/glEnd.")
        return -1

    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1
    #image.show()
    return texture

# **********************************************************************
#  Habilita o uso de textura 'NroDaTextura'
#  Se 'NroDaTextura' <0, desabilita o uso de texturas
#  Se 'NroDaTextura' for maior que a quantidade de texturas, gera
#  mensagem de erro e desabilita o uso de texturas
# **********************************************************************
def useTexture (NroDaTextura: int):
    global texturas
    if (NroDaTextura>len(texturas)):
        print ("Numero invalido da textura.")
        glDisable (GL_TEXTURE_2D)
        return
    if (NroDaTextura < 0):
        glDisable (GL_TEXTURE_2D)
    else:
        glEnable (GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texturas[NroDaTextura])


# **********************************************************************
#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
#
# **********************************************************************
def reshape(w: int, h: int):
    global AspectRatio
    # Evita divisÃ£o por zero, no caso de uam janela com largura 0.
    if h == 0:
        h = 1
    # Ajusta a relaÃ§Ã£o entre largura e altura para evitar distorÃ§Ã£o na imagem.
    # Veja funÃ§Ã£o "PosicUser".
    AspectRatio = w / h
    # Reset the coordinate system before modifying
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    glViewport(0, 0, w, h)

    PosicUser()
# **********************************************************************
def DefineLuz():
    # Define cores para um objeto dourado
    LuzAmbiente = [0.4, 0.4, 0.4]
    LuzDifusa   = [0.7, 0.7, 0.7]
    LuzEspecular = [0.9, 0.9, 0.9]
    PosicaoLuz0  = [2.0, 3.0, 0.0 ]  # PosiÃ§Ã£o da Luz
    Especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable ( GL_COLOR_MATERIAL )

    #Habilita o uso de iluminaÃ§Ã£o
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, LuzAmbiente)
    # Define os parametros da luz nÃºmero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, LuzAmbiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LuzDifusa  )
    glLightfv(GL_LIGHT0, GL_SPECULAR, LuzEspecular  )
    glLightfv(GL_LIGHT0, GL_POSITION, PosicaoLuz0 )
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT,GL_SPECULAR, Especularidade)

    # Define a concentraÃ§Ã£oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serÃ¡ o brilho. (Valores vÃ¡lidos: de 0 a 128)
    glMateriali(GL_FRONT,GL_SHININESS,51)

# **********************************************************************
# DesenhaCubos()
# Desenha o cenario
#
# **********************************************************************
# def DesenhaCubo():
#     glutSolidCube(1)
def DesenhaCubo(tamAresta):
    glBegin ( GL_QUADS )
    # // Front Face
    glNormal3f(0,0,1)
    glVertex3f(-tamAresta/2, -tamAresta/2,  tamAresta/2)
    glVertex3f( tamAresta/2, -tamAresta/2,  tamAresta/2)
    glVertex3f( tamAresta/2,  tamAresta/2,  tamAresta/2)
    glVertex3f(-tamAresta/2,  tamAresta/2,  tamAresta/2)
    # // Back Face
    glNormal3f(0,0,-1)
    glVertex3f(-tamAresta/2, -tamAresta/2, -tamAresta/2)
    glVertex3f(-tamAresta/2,  tamAresta/2, -tamAresta/2)
    glVertex3f( tamAresta/2,  tamAresta/2, -tamAresta/2)
    glVertex3f( tamAresta/2, -tamAresta/2, -tamAresta/2)
    # // Top Face
    glNormal3f(0,1,0)
    glVertex3f(-tamAresta/2,  tamAresta/2, -tamAresta/2)
    glVertex3f(-tamAresta/2,  tamAresta/2,  tamAresta/2)
    glVertex3f( tamAresta/2,  tamAresta/2,  tamAresta/2)
    glVertex3f( tamAresta/2,  tamAresta/2, -tamAresta/2)
    # // Bottom Face
    glNormal3f(0,-1,0)
    glVertex3f(-tamAresta/2, -tamAresta/2, -tamAresta/2)
    glVertex3f( tamAresta/2, -tamAresta/2, -tamAresta/2)
    glVertex3f( tamAresta/2, -tamAresta/2,  tamAresta/2)
    glVertex3f(-tamAresta/2, -tamAresta/2,  tamAresta/2)
    # // Right face
    glNormal3f(1,0,0)
    glVertex3f( tamAresta/2, -tamAresta/2, -tamAresta/2)
    glVertex3f( tamAresta/2,  tamAresta/2, -tamAresta/2)
    glVertex3f( tamAresta/2,  tamAresta/2,  tamAresta/2)
    glVertex3f( tamAresta/2, -tamAresta/2,  tamAresta/2)
    # // Left Face
    glNormal3f(-1,0,0)
    glVertex3f(-tamAresta/2, -tamAresta/2, -tamAresta/2)
    glVertex3f(-tamAresta/2, -tamAresta/2,  tamAresta/2)
    glVertex3f(-tamAresta/2,  tamAresta/2,  tamAresta/2)
    glVertex3f(-tamAresta/2,  tamAresta/2, -tamAresta/2)
    glEnd()


def PosicUser():

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    # glViewport(0, 0, 500, 500)
    #print ("AspectRatio", AspectRatio)

    carregaPosicObs()

    gluPerspective(70,AspectRatio,0.01,50) # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        posicaoObs.x, posicaoObs.y, posicaoObs.z, # Posição do Observador
        alvoObs.x, alvoObs.y, alvoObs.z, # Posição do Alvo
        0,1.0,0)

def carregaPosicObs():
    global posicaoObs, alvoObs
    if primeiraPessoa:
        posicaoObs.x = posCarro.x
        posicaoObs.y = posCarro.y + 1
        posicaoObs.z = posCarro.z


        # alvoObs.x = posCarro.x
        # alvoObs.y = posCarro.y
        # # Porque precisa desse -0.1?
        # alvoObs.z = posCarro.z - 0.1
        alvoObs = posicaoObs.__add__(dirCarro)
    else:
        posicaoObs.x = posCarro.x
        posicaoObs.y = posCarro.y + 12
        posicaoObs.z = posCarro.z

        alvoObs.x = posCarro.x
        alvoObs.y = posCarro.y
        # Porque precisa desse -0.1?
        alvoObs.z = posCarro.z - 0.1

def desenhaCarro():
    glPushMatrix()
    glTranslated(posCarro.x, posCarro.y, posCarro.z)
    glRotatef(anguloSomatorio, 0, 1, 0)
    glRotatef(180, 0, 1, 0)

    glColor3f(00.576471,0.858824,0.439216)

    # glutSolidSphere(0.5, 5, 5)
    # glutSolidCone(0.5, 1, 20, 20)

    desenhaRec(1, 1, 2)

    glTranslatef(0.4, 0.4, 1.1)
    glColor3f(0.309804,0.184314,0.184314)
    desenhaRec(0.1, 0.2, 0.2)


    glTranslatef(-0.8, 0, 0)
    glColor3f(0.309804,0.184314,0.184314)
    desenhaRec(0.1, 0.2, 0.2)

    # glTranslatef(-1+0.2, 0, 0)
    # glColor3f(0.309804,0.184314,0.184314)
    # desenhaRec(0.1, 0.2, 0.2)

    glPopMatrix()

# ToDo: Corrigi bugs no retangulo
def desenhaRec(x, y, z):
    glPushMatrix()

    glScaled(x, y, z)
    DesenhaCubo(1)

    glPopMatrix()

# **********************************************************************
# void DesenhaLadrilho(int corBorda, int corDentro)
# Desenha uma cÃ©lula do piso.
# O ladrilho tem largula 1, centro no (0,0,0) e estÃ¡ sobre o plano XZ
# **********************************************************************
def DesenhaLadrilho(texturaId):

    if texturaId < 0 or texturaId > 12:
        texturaId = 5
    useTexture(texturaId)

    glColor3f(1,1,1)
    glBegin ( GL_QUADS )
    glNormal3f(0,1,0)
    glTexCoord(1,1)
    glVertex3f(-1,  0.0, -1)
    glTexCoord(1,0)
    glVertex3f(-1,  0.0,  1)
    glTexCoord(0,0)
    glVertex3f( 1,  0.0,  1)
    glTexCoord(0,1)
    glVertex3f( 1,  0.0, -1)
    glEnd()

    # glColor3f(1,1,1) # desenha a borda da QUAD
    # glBegin ( GL_LINE_STRIP )
    # glNormal3f(0,1,0)
    # glVertex3f(-1,  0.0, -1)
    # glVertex3f(-1,  0.0,  1)
    # glVertex3f( 1,  0.0,  1)
    # glVertex3f( 1,  0.0, -1)
    # glEnd()

def desenhaPredio(altura):
    glColor3f(0.5,0.0,0.0) # Vermelho
    desenhaRec(2,altura,2)

# **********************************************************************
first = True
def DesenhaPiso():
    global first
    glPushMatrix()

    glTranslated(0,-1,0)
    for linhaZ in reversed(mapa):
        glPushMatrix()
        for colX in reversed(linhaZ):
            # if first:
            #     print(colX, end=' ')
            DesenhaLadrilho(colX-1)
            # DesenhaLadrilho(6)

            if colX > 14:
                desenhaPredio(colX)

            glTranslated(2, 0, 0)
        glPopMatrix()
        glTranslated(0, 0, 2)

        # if first:
        #     print('\n')

    first = False
    glPopMatrix()


# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
#
# **********************************************************************
def display():
    global Angulo
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    DefineLuz()
    PosicUser()

    glMatrixMode(GL_MODELVIEW)


    DesenhaPiso()
    glColor3f(0.5,0.0,0.0) # Vermelho
    glPushMatrix()
    glTranslatef(5, 0, 3)
    glRotatef(Angulo,0,1,0)
    DesenhaCubo(1)
    glPopMatrix()

    glColor3f(0.6156862745, 0.8980392157, 0.9803921569) # Amarelo
    glPushMatrix()
    glTranslatef(-4, 0, 2)
    glRotatef(-Angulo,0,1,0)
    DesenhaCubo(1)
    glPopMatrix()

    glColor3f(0.439216,0.858824,0.576471) # Amarelo
    glPushMatrix()
    glTranslatef(-10, 0, 10)
    glRotatef(-Angulo,0,1,0)
    DesenhaCubo(1)
    glPopMatrix()

    # glColor3f(00.576471,0.858824,0.439216) # Amarelo
    # glPushMatrix()
    # glTranslatef(0, 0, 10)
    # glRotatef(-Angulo,0,1,0)
    # DesenhaCubo(1)
    # glPopMatrix()

    glColor3f(0.309804,0.184314,0.184314) # Amarelo
    glPushMatrix()
    glTranslatef(10, 0, 10)
    glRotatef(-Angulo,0,1,0)
    DesenhaCubo(1)
    glPopMatrix()

    # glColor3f(0.309804,0.184314,0.184314) # Amarelo
    glPushMatrix()
    glTranslatef(pontoGas.x, pontoGas.y, pontoGas.z)
    DesenhaCubo(1)
    glPopMatrix()

    Angulo = Angulo + 1

    desenhaCarro()

    if moving:
        moveFrente()

    glutSwapBuffers()


# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1

    if AccumDeltaT > 1.0/30:  # fixa a atualizaÃ§Ã£o da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()



# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
#
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    global image, alvoObs, moving, primeiraPessoa
    vetorAlvo = Ponto.__add__(alvoObs, Ponto.__mul__(posicaoObs, -1))
    #print (args)
    # If escape is pressed, kill everything.

    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)         # a tecla ESC for pressionada

    if args[0] == b' ':
        moving = not moving
        # init()

    if args[0] == b'i':
        image.show()

    if args[0] == b'a':
        giraEsquerda()

    if args[0] == b'd':
        giraDireita()

    if args[0] == b'w':
        moveFrente()

    if args[0] == b's':
        moveTras()

    if args[0] == b'p':
        primeiraPessoa = not primeiraPessoa


    # ForÃ§a o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )
# **********************************************************************

def arrow_keys(a_keys: int, x: int, y: int):
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        giraCima()
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        giraBaixo()
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        giraEsquerda()
        pass
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        giraDireita()
        pass

    glutPostRedisplay()

def isPosicaoValida(posicao: Ponto):
    global gasTotal
    conversorZ = 60 / tamMapaZ
    mapaZ =  round(posicao.z / conversorZ)
    conversorX = 60 / tamMapaX
    mapaX = round(posicao.x / conversorX)

    try:
        print("FOOOOI")
        print("mapaX : ", mapaX)
        print("mapaZ: ", mapaZ)
        print("Matriz: ", mapa[tamMapaZ - abs(mapaZ) -1][tamMapaX - abs(mapaX) -1])
        print("mapaGas: ", mapaGas)
        print("\n")
        print("Linha: ", tamMapaZ - abs(mapaZ) -1)
        print("Coluna : ", tamMapaX - abs(mapaX) -1)
        if (mapaX == mapaGas[0] and mapaZ == mapaGas[1]):
            gasTotal = 100
            carregaGasolina()
        # return True
        return mapaX >= 0 and mapaX < 30 and mapaZ >= 0 and mapaZ < 30 and mapa[tamMapaZ - abs(mapaZ) -1][tamMapaX - abs(mapaX) -1] != 0
    except IndexError:
        print("EROROOO")
        return False

def moveFrente():
    global posCarro, gasTotal

    vetorAlvo = Ponto.__mul__(Ponto.versor(dirCarro), velCarro)
    novaPosicao = Ponto.__add__(posCarro, vetorAlvo)

    novaPosicao.imprime("Posicao: ")

    if gasTotal <= 0:
        print("ACABOU!")
        return

    if (isPosicaoValida(novaPosicao)):
        posCarro = novaPosicao
        gasTotal -= 0.2


def moveTras():
    global posCarro

    vetorAlvo = Ponto.__mul__(Ponto.__mul__(Ponto.versor(dirCarro), -1), velCarro)
    novaPosicao = Ponto.__add__(posCarro, vetorAlvo)
    novaPosicao.imprime("Nova Posição: ")

    if (isPosicaoValida(novaPosicao)):
        posCarro = novaPosicao

def giraEsquerda():
    global dirCarro, anguloSomatorio

    # dirCarro.imprime(" ANTES - Dir Carro: ")
    anguloSomatorio = anguloSomatorio + anguloRotacao
    dirCarro = dirCarro.rotacionaY(anguloRotacao)
    # dirCarro.imprime("DEPOIS - Dir Carro: ")

def giraDireita():
    global dirCarro, anguloSomatorio

    # dirCarro.imprime(" ANTES - Dir Carro: ")
    anguloSomatorio = anguloSomatorio - anguloRotacao
    dirCarro = dirCarro.rotacionaY(-anguloRotacao)
    # dirCarro.imprime("DEPOIS - Dir Carro: ")

def giraCima():
    global posicaoObs, alvoObs
    vetorAlvo = Ponto.__add__(alvoObs, Ponto.__mul__(posicaoObs, -1))
    # mul = -1 if vetorAlvo.z > 0 else 1
    mul = 1
    print('mul: ', mul)
    vetorRotacionado = vetorAlvo.rotacionaX(anguloRotacao*mul)
    vetorAlvo.imprime("Vetor alvo: ")
    vetorRotacionado.imprime("Vetor rotacionado: ")


    alvoObs = Ponto.__add__(vetorRotacionado, posicaoObs)

def giraBaixo():
    global posicaoObs, alvoObs
    vetorAlvo = Ponto.__add__(alvoObs, Ponto.__mul__(posicaoObs, -1))
    # mul = 1 if vetorAlvo.z > 0 else -1
    mul = -1
    print('mul: ', mul)
    vetorRotacionado = vetorAlvo.rotacionaX(anguloRotacao*mul)
    vetorAlvo.imprime("Vetor alvo: ")
    vetorRotacionado.imprime("Vetor rotacionado: ")

    alvoObs = Ponto.__add__(vetorRotacionado, posicaoObs)

def carregaMatrizMapa():
    global mapa, tamMapaX, tamMapaZ
    arquivoMapa = open("Mapa1.txt", "r")
    sizes = arquivoMapa.readline().split(" ")

    tamMapaX = int(sizes[0])
    tamMapaZ = int(sizes[1])

    print("tamMapaX: ", tamMapaX)

    linhas = arquivoMapa.read().splitlines()

    for linha in linhas:
        print(linha)
        print('-----')
        mapa.append([int(x) for x in linha.split("\t")])

    # for i in range(mapa) :
    #     mapa[i] = reversed(mapa[i])

    print(mapa)

def mouse(button: int, state: int, x: int, y: int):
    glutPostRedisplay()

def mouseMove(x: int, y: int):
    glutPostRedisplay()

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

carregaMatrizMapa()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA|GLUT_DEPTH | GLUT_RGB)
glutInitWindowPosition(0, 0)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(650, 500)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de tÃ­tulo da janela.
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("OpenGL 3D")

# executa algumas inicializaÃ§Ãµes
init ()

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# serÃ¡ chamada automaticamente quando
# for necessÃ¡rio redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc (animate)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# serÃ¡ chamada automaticamente quando
# o usuÃ¡rio alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# serÃ¡ chamada automaticamente sempre
# o usuÃ¡rio pressionar uma tecla comum
glutKeyboardFunc(keyboard)

# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" serÃ¡ chamada
# automaticamente sempre o usuÃ¡rio
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)

#glutMouseFunc(mouse)
#glutMotionFunc(mouseMove)


try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass