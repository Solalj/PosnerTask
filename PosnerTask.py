#! /usr/bin/env python
import random
from expyriment import design, control, stimuli, misc

# Constants relative to the trials
N_TRIALS = 20
WAITING_TIME_BETWEEN_TRIALS = 2000 
WAITING_TIME_BETWEEN_INITIAL_AND_CUE = 2000 
WAITING_TIME_BETWEEN_CUE_AND_TARGET = 200 
MAX_RESPONSE_DELAY = 30000

# Constants relative to the square/rectangle
RECT_SIZE = (150, 150)
RECT_COLOR = (250, 250, 250)
RECT_THIN = 3
RECT_THICK = 10
RECT_XPOS = 300

# Constants relative to the stars
STAR_SIZE = (50, 50)
STAR_WIDTH = 5
STAR_COLOUR = (250, 250, 250)
STAR_XPOS = 300

# Colour of the backgroung of the experiment
SCREEN_COLOUR = (0, 0, 0)

# Check that the number of trials is even, otherwise the experiment will not run
if(N_TRIALS%2 != 0):
    raise Exception("Veuillez rentrer un nomre d'essai pair !")

# Creation of the experiment 
exp = design.Experiment(name="PosnerTask", text_size=20)
control.initialize(exp)

# Fixing cross in center of screen
Cross = stimuli.FixCross(size=(50, 50), line_width=5, colour=(250, 250, 250)) 

# This is the function to create the rectangles/squares on the right and left
def rectangle(thickness, side):
    width = (RECT_THIN if thickness == 'Thin' else RECT_THICK)
    pos = RECT_XPOS if side == 'Right' else -RECT_XPOS 
    return stimuli.Rectangle(RECT_SIZE, 
                             colour=RECT_COLOR,
                             line_width = width, 
                             position=(pos, 0))

# This is the function to create the stars corresponding to the targets
def star(side):
    if (side == 'Right') :
        StarRight    = stimuli.FixCross(size = STAR_SIZE, line_width = STAR_WIDTH, colour = STAR_COLOUR,position = (STAR_XPOS, 0))
        CrossRotate = stimuli.FixCross(size = STAR_SIZE, line_width = STAR_WIDTH, colour = STAR_COLOUR)
        CrossRotate.native_rotate(45.0)
        CrossRotate.plot(StarRight)  
        return StarRight  
    else :
        StarLeft    = stimuli.FixCross(size = STAR_SIZE, line_width = STAR_WIDTH, colour = STAR_COLOUR,position = (-STAR_XPOS, 0))
        CrossRotate = stimuli.FixCross(size = STAR_SIZE, line_width = STAR_WIDTH, colour = STAR_COLOUR)
        CrossRotate.native_rotate(45.0)
        CrossRotate.plot(StarLeft)
        return StarLeft

# This is the function that create a screen that will be added to the trials
def screen(rect_thickness_left, rect_thickness_right, cross_or_not, star_side = None) :
    background_screen = stimuli.BlankScreen(colour = SCREEN_COLOUR)
    rectangle(rect_thickness_right, 'Right').plot(background_screen)
    rectangle(rect_thickness_left, 'Left').plot(background_screen)
    if cross_or_not :
        Cross.plot(background_screen) 
    else :
        star(star_side).plot(background_screen)
    return background_screen

# This is the function that bind three screens to create the full trial
def trial(congruent_or_not,
          side_target) :
    List_screen = design.Trial()
    List_screen.add_stimulus(screen('Thin', 'Thin', True))
    if (congruent_or_not == 'Congruent'):
        List_screen.set_factor("Congruency", 'Congruent') 
        if (side_target == 'Right'):
            List_screen.add_stimulus(screen('Thin', 'Thick', True))
            List_screen.add_stimulus(screen('Thin', 'Thin', False, 'Right'))
            List_screen.set_factor("Side", 'Right')
        else :
            List_screen.add_stimulus(screen('Thick', 'Thin', True))
            List_screen.add_stimulus(screen('Thin', 'Thin', False, 'Left'))
            List_screen.set_factor("Side", "Left") 
    else :
        List_screen.set_factor("Congruency", "Incongruent") 
        if (side_target == 'Right'):
            List_screen.add_stimulus(screen('Thick', 'Thin', True))
            List_screen.add_stimulus(screen('Thin', 'Thin', False, 'Right'))
            List_screen.set_factor("Side", "Right") 
        else :
            List_screen.add_stimulus(screen('Thin', 'Thick', True))
            List_screen.add_stimulus(screen('Thin', 'Thin', False, 'Left'))
            List_screen.set_factor("Side", "Left") 
    return List_screen

# This create the list of the different trials 
liste_trials = []
for i in range(N_TRIALS//4) :
    liste_trials.append(trial('Congruent', 'Left')) # This create a 1/4 of the trials congruent on the right
for j in range(N_TRIALS//4) :
    liste_trials.append(trial('Congruent', 'Right'))
for k in range(N_TRIALS//4) :
    liste_trials.append(trial('Incongruent', 'Left'))
for l in range(N_TRIALS//4) :
    liste_trials.append(trial('Incongruent', 'Right'))
random.shuffle(liste_trials)
blankscreen = stimuli.BlankScreen()

# This is this instructions at the beggining of the experiment
instructions = stimuli.TextScreen("Instructions",
    f"""You will partcipate to a attentional studie.

    You will see a fixation cross in the center of the screen with two squares on the right and the left.
    
    One of the two squares will become thick either on the right or left. 
    You still need to focus on the fixation cross in the middle. Don't look at the bold square

    Then, a star will appear either in the right square or in the left square. You can look at it.
    You need to tap as fast as possible on the lettre F if the star appear on the left and J if the star appear on the right.

    Their will be {N_TRIALS} trials in total. 

    Press the spacebar to start.
    
    Thank you for participating in my experiment.""")

exp.add_data_variable_names(['Type de trial',
                            'Touche utilise',
                            'Quelle est la touche attendu',
                            'Temps de reaction', 
                            'Congruent / Incongruent',
                            'Right / Left',
                            'Temps d attente entre les trials', 
                            'Temps d attente entre l ecran initiale et l indice', 
                            'Temps d attente entre l indice et la cible'])

control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait(keys = [misc.constants.K_SPACE])

# Correct_key is the key that the person will need to press, either "f" if it is on the left or "j" if it is on the right
correct_key = None

# This for loop is where everything is assembled
for trial in liste_trials :
    compteur_stimuli = 0 # I create a counter of stimuli to get to wich screen we are
    stimuli.BlankScreen(colour = SCREEN_COLOUR).present()
    exp.clock.wait(WAITING_TIME_BETWEEN_TRIALS)
    for stimulus in trial.stimuli :
        compteur_stimuli = compteur_stimuli + 1
        stimulus.present()
        if (compteur_stimuli == 1) :
            exp.clock.wait(WAITING_TIME_BETWEEN_INITIAL_AND_CUE)
        if (compteur_stimuli == 2) :
            exp.clock.wait(WAITING_TIME_BETWEEN_CUE_AND_TARGET)
        if (compteur_stimuli == 3) :
            key, rt = exp.keyboard.wait(keys = [misc.constants.K_f, misc.constants.K_j], duration = MAX_RESPONSE_DELAY) 
        if (trial.get_factor('Side') == "Right") :
            correct_key = "j"
        if (trial.get_factor('Side') == "Left") :
            correct_key = "f"
    exp.data.add([stimulus, 
                key,
                correct_key,
                rt, 
                trial.get_factor("Congruency"), 
                trial.get_factor("Side"), 
                WAITING_TIME_BETWEEN_TRIALS, 
                WAITING_TIME_BETWEEN_INITIAL_AND_CUE, 
                WAITING_TIME_BETWEEN_CUE_AND_TARGET])

control.end()