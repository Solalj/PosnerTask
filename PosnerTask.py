#! /usr/bin/env python
# Time-stamp: <2021-03-23 22:02:10 christophe@pallier.org>
# License: Creative Commons Attribution-ShareAlike CC BY-SA

import random
from expyriment import design, control, stimuli

N_TRIALS = 20  # nombre d'essai
SQUARE_TIME_1 = 500 # temps de presentation des carres 1
CUE_TIME = 100 # temps de presentation de l'indice
SQUARE_TIME_1 = 100 # temps de presentation des carres 2
TARGET_TIME = 150 # temps de presentation de la cible
RESULT_FILE = 'reaction_times.csv'

exp = design.Experiment(name="PosnerTask", text_size=20)
#control.set_develop_mode(on=True)
control.initialize(exp)

RectangleLeft = stimuli.Rectangle((200, 200), colour=(250, 250, 250), line_width=5, position=(250, 0))
RectangleRight = stimuli.Rectangle((200, 200), colour=(250, 250, 250), line_width=5, position=(-250, 0))
RectangleBoldLeft = stimuli.Rectangle((200, 200), colour=(250, 250, 250), line_width=5, position=(250, 0))
RectangleBoldRight = stimuli.Rectangle((200, 200), colour=(250, 250, 250), line_width=5, position=(-250, 0))
Cross = stimuli.FixCross(size=(50, 50), line_width=5, colour=(0, 0, 0))
Star = stimuli.Shape(position=None, colour=None, line_width=None, anti_aliasing=None, vertex_list=None, debug_contour_colour=None)
Star.add_vertices([(10,0), (0, -0.2), (-10, 0.2), (8, -8), (-0.2, 0), (-7.8, 8), (0, -10), (-0.2, 0), (0.2, 10), (-8, 8), (0, -0.2), (8, 7.8), (-10,0), (0, 0.2), (10, -0.2), (-8, 8), (0.2, 0), (7.8, -8), (0, 10), (0.2, 0), (-0.2, -10), (8, -8), (0, -0.2), (-8, -7.8)])

def display_instruction(screen, x, y):
    myfont = pygame.font.SysFont(pygame.font.get_fonts()[0], 32)
    line1 = myfont.render("You will see two squares appear on your screen around a cross. Please look at the cross.", 1, pygame.Color('white'))
    line2 = myfont.render("Then, you will see one of the two squares in bold. Please, keep your eyes on the cross.", 1, pygame.Color('white'))
    line3 = myfont.render("When you see a star appear in one of the two squares, please, press the SPACE BAR as quickly as possible.", 1, pygame.Color('white'))
    line4 = myfont.render("Press it now to start!", 1, pygame.Color('white'))
    screen.blit(line1, (x, y))
    screen.blit(line2, (x, y + 60))
    pygame.display.flip()

