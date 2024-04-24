#! /usr/bin/env python
# Time-stamp: <2021-03-23 22:02:10 christophe@pallier.org>
# License: Creative Commons Attribution-ShareAlike CC BY-SA

import random
from expyriment import design, control, stimuli

N_TRIALS = 20  # Nombre d'essai
SQUARE_TIME_1 = 500 # Temps de presentation des carres 1
CUE_TIME = 100 # Temps de presentation de l'indice
SQUARE_TIME_1 = 100 # Temps de presentation des carres 2
TARGET_TIME = 150 # Temps de presentation de la cible
RESULT_FILE = 'reaction_times.csv'

if(N_TRIALS%2 != 0):
    raise Exception("Veuillez rentrer un nomre d'essai pair !")

exp = design.Experiment(name="PosnerTask", text_size=20)
#control.set_develop_mode(on=True)
control.initialize(exp)


RectangleLeft      = stimuli.Rectangle((200, 200), colour=(250, 250, 250), line_width=3, position=(250, 0))
RectangleRight     = stimuli.Rectangle((200, 200), colour=(250, 250, 250), line_width=3, position=(-250, 0))
RectangleBoldLeft  = stimuli.Rectangle((200, 200), colour=(250, 250, 250), line_width=10, position=(250, 0))
RectangleBoldRight = stimuli.Rectangle((200, 200), colour=(250, 250, 250), line_width=10, position=(-250, 0))

StarLeft           = stimuli.FixCross(size=(50, 50), line_width=5, colour=(250, 250, 250),position = (-250, 0))
CrossRotate        = stimuli.FixCross(size=(50, 50), line_width=5, colour=(250, 250, 250))
CrossRotate.native_rotate(45.0)
CrossRotate.plot(StarLeft)

StarRight          = stimuli.FixCross(size=(50, 50), line_width=5, colour=(250, 250, 250),position = (250, 0))
CrossRotate        = stimuli.FixCross(size=(50, 50), line_width=5, colour=(250, 250, 250))
CrossRotate.native_rotate(45.0)
CrossRotate.plot(StarRight)

Cross = stimuli.FixCross(size=(50, 50), line_width=5, colour=(250, 250, 250))

# Creation de differents ecrans que je pourrais alterner dans une liste
ScreenInit = stimuli.BlankScreen(colour = (0, 0, 0)) # Ecran initial
Cross.plot(ScreenInit)
RectangleLeft.plot(ScreenInit)
RectangleRight.plot(ScreenInit)

ScreenCueLeft = stimuli.BlankScreen(colour = (0, 0, 0)) # Ecran avec l'indice a gauche
Cross.plot(ScreenCueLeft)
RectangleBoldLeft.plot(ScreenCueLeft)
RectangleRight.plot(ScreenCueLeft)

ScreenCueRight = stimuli.BlankScreen(colour = (0, 0, 0)) # Ecran avec l'indice a droite
Cross.plot(ScreenCueRight)
RectangleBoldRight.plot(ScreenCueRight)
RectangleLeft.plot(ScreenCueRight)

ScreenTargetLeft = stimuli.BlankScreen(colour = (0, 0, 0)) # Ecran avec la cible a gauche
RectangleRight.plot(ScreenTargetLeft)
RectangleLeft.plot(ScreenTargetLeft)
StarLeft.plot(ScreenTargetLeft)

ScreenTargetRight = stimuli.BlankScreen(colour = (0, 0, 0)) # Ecran avec la cible a droite
RectangleRight.plot(ScreenTargetRight)
RectangleLeft.plot(ScreenTargetRight)
StarRight.plot(ScreenTargetRight)

ListCongruentLeft = []
ListCongruentLeft.append(ScreenInit)
ListCongruentLeft.append(ScreenCueLeft)
ListCongruentLeft.append(ScreenTargetLeft)

ListCongruentRight = []
ListCongruentRight.append(ScreenInit)
ListCongruentRight.append(ScreenCueRight)
ListCongruentRight.append(ScreenTargetRight)

ListIncongruentLeft = []
ListIncongruentLeft.append(ScreenInit)
ListIncongruentLeft.append(ScreenCueLeft)
ListIncongruentLeft.append(ScreenTargetRight)

ListCongruentRight = []
ListCongruentRight.append(ScreenInit)
ListCongruentRight.append(ScreenCueRight)
ListCongruentRight.append(ScreenTargetLeft)


def display_instruction(screen, x, y):
    myfont = pygame.font.SysFont(pygame.font.get_fonts()[0], 32)
    line1 = myfont.render("You will see two squares appear on your screen around a cross. Please look at the cross.", 1, pygame.Color('white'))
    line2 = myfont.render("Then, you will see one of the two squares in bold. Please, keep your eyes on the cross.", 1, pygame.Color('white'))
    line3 = myfont.render("When you see a star appear in one of the two squares, please, press the SPACE BAR as quickly as possible.", 1, pygame.Color('white'))
    line4 = myfont.render("Press it now to start!", 1, pygame.Color('white'))
    screen.blit(line1, (x, y))
    screen.blit(line2, (x, y + 60))
    pygame.display.flip()

