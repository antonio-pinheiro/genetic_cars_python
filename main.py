# -*- coding: utf-8 -*-

##############################################################################
##																			##
##			              Genetic Cars - TCC			                    ##
##																		   	##
##				                                        				   	##
##																			##
##############################################################################
##																			##
##	Project:		Genetic Cars 											##
##															     			##
##	File name:		main.py 												##
##																			##
##	Created by:		Antônio Pinheiro and Iane Rodrigues			            ##
##																			##
##	Description:	Demonstrates Genetic Algorithm Functionalities	        ##
##	                                                                        ##
##  Date:           05/07/2021                                              ##
##############################################################################

# Imported libraries
import random
import os
import sys
import numpy
import matplotlib.pyplot as plt
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from deap import base
from deap import creator
from deap import algorithms
from deap import tools
from typing import Tuple, Any


surface = create_example_window('Genetic Cars', (1280, 720))

def rendering_menu_images(img_selection):
    
    # Constants defined as global, their values ​​do not change during execution.
    global buttons_dict
    global render_buttons_dict
    
    buttons_dict = {}
    render_buttons_dict = {}
    
    buttons_dict["back_img"] = pygame.image.load("/home/tony/Documents/fatec_tg/genetic_cars_python_tg/Menu/back_button.png").convert_alpha()
    buttons_dict["close_img"] = pygame.image.load("/home/tony/Documents/fatec_tg/genetic_cars_python_tg/Menu/close_button.png").convert_alpha()
    
    render_buttons_dict["back_menu"] = buttons_dict["back_img"].get_rect()
    render_buttons_dict["back_menu"].center = 1280//12, 720//14
    render_buttons_dict["close_menu"] = buttons_dict["close_img"].get_rect()
    render_buttons_dict["close_menu"].center = 1280//1.1, 720//14
    
    # Configure and rendering background screen.
    pygame.display.set_caption("Genetic Cars")
    screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    img_selection
    background = pygame.image.load(img_selection).convert()
    screen.blit(background, (0, 0))
    
    # Rendering Back button and Close button in screen.
    screen.blit(buttons_dict["back_img"], render_buttons_dict["back_menu"])
    pygame.draw.rect(screen,(0,0,0), render_buttons_dict["back_menu"], 1)
    screen.blit(buttons_dict["close_img"], render_buttons_dict["close_menu"])
    pygame.draw.rect(screen,(0,0,0), render_buttons_dict["close_menu"], 1)
    pygame.display.update()
    

# Function responsible for execution of demonstration after selection of difficulty level.
def start_demonstration():
    
    
    # Open results and subscribe information about last execution.
    pygame_results = open('results/output.txt', 'w')

    # Structure of Genetic Algorithm, developed with DEAP library,
    # responsible for generating and select the better individual within a population.
    class Pilot:

        def __init__(self, name, speed, pilot_performance, course):
            self.name = name
            self.pilot_performance = pilot_performance
            self.speed = speed
            self.course = course

    # Open a file that has the pilot names, pilot_names.txt. 
    list_pilot = open("results/pilot_names.txt", "r")
    pilot_names_list = []
    pilots = []

    # Generate a list with pilot names, read from the pilot_names.txt.
    for genetic_pilot in list_pilot:
        genetic_pilot = genetic_pilot.strip()
        pilot_names_list.append(genetic_pilot)
    list_pilot.close()

    # Generate a list with pilot names to construct pilots objects, 
    # read from pilot_names_list.
    for j in range(0, len(pilot_names_list)):
        pilots.append(
            Pilot(pilot_names_list[j], random.randrange(initial_value, final_value), random.randrange(108, 135),
                  30.000))

    # Initialization of lists that has attributes of object Pilot, 
    # will use these lists in Genetic Algorithm during its execution.
    names = []
    pilot_performances = []
    speeds = []
    courses = []

    # Construction lists with pilot attributes.
    for pilot in pilots:
        pilot_performances.append(pilot.pilot_performance)
        speeds.append(pilot.speed)
        names.append(pilot.name)
        courses.append(pilot.course)
    limit

    # DEAP ambient initialization and configuration.
    toolbox = base.Toolbox()
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_bool, n=len(pilot_performances))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Evaluation function, indicate which are the best pilots in a population.
    def evaluation(individual):
        grade = 0
        sum_times = 0

        for i in range(len(individual)):
            if individual[i] == 1:
                grade += pilot_performances[i]
                sum_times += courses[i] / speeds[i]

        if sum_times > limit:
            grade = 1
        return grade / 100000,

    # DEAP functions and parameters
    toolbox.register("evaluate", evaluation)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.01)
    toolbox.register("select", tools.selRoulette)

    if __name__ == "__main__":

        random.seed(1)
        population = toolbox.population(n=22)
        crossover_probability = 1.0
        mutation_probability = 0.01
        generations = 100

        # Statistics generated and information about population using numpy.
        statistics = tools.Statistics(key=lambda individual: individual.fitness.values)
        statistics.register("Maximum", numpy.max)
        statistics.register("Minimum", numpy.min)
        statistics.register("Mean", numpy.mean)
        statistics.register("Standard", numpy.std)

        population, info = algorithms.eaSimple(population, toolbox,
                                               crossover_probability,
                                               mutation_probability,
                                               generations, statistics)
        best = tools.selBest(population, 1)

        # Print information about better pilot in a terminal
        # and save in a file called output.txt to read with PyGame.
        for individual in best:
            print(individual)
            print(individual.fitness)
            sum_performance = 0
            sum_times = 0

            for i in range(len(pilots)):
                if individual[i] == 1:
                    sum_performance += pilot_performances[i]
                    sum_times += courses[i] / speeds[i]

                    with open('results/output.txt', 'a+') as results:

                        results.seek(0)
                        data = results.read(100)
                        if len(data) > 0:
                            results.write("\n")

                        print(level + "Pilot: %s / Grade - %s \n" % (pilots[i].name,
                                                                     pilots[i].pilot_performance), file=results)

                    print(level + "Pilot: %s  / Grade: %s \n" % (pilots[i].name,
                                                                 pilots[i].pilot_performance))

            print("Best Solution: %s - Sum of Limits %s" % (sum_performance, sum_times))

        # Pyplot, generate graphics about execution.
        graphic_results = info.select("Maximum")
        plt.plot(graphic_results)
        plt.title("Monitoring of evolution")
        plt.xlabel("generation")
        plt.ylabel("Grade")
        plt.show()

        # Structure responsible for show images with pygame after ends of Genetic Cars execution.
        pygame.init()
        position_y = 640
        position_y_update = 0
        x = 50
        y = 630
        z = 305
        screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        clock = pygame.time.Clock()
        font = pygame.font.SysFont('Arial', 18, True, True)
        rendering_menu_images('Background/track.png')

        
        # Open a file that has the pilot names, pilot_names.txt. 
        list_pilot = open("results/pilot_names.txt", "r")

        # Generate a list with pilot names, read from the pilot_names.txt.
        for genetic_pilot in list_pilot:
            genetic_pilot = genetic_pilot.strip()
            pilot_names_list.append(genetic_pilot)
        list_pilot.close()

        # Load the car images that are inside a directory "cars", in a dictionary.
        # The key from dictionary has the name of loaded image
        # and value has the PyGame parameters of images.
        image_dict = {}
        for cars_img in os.listdir('/home/tony/Documents/fatec_tg/genetic_cars_python_tg/Cars'):
            if cars_img.endswith('.png'):
                path = os.path.join('/home/tony/Documents/fatec_tg/genetic_cars_python_tg/Cars', cars_img)
                key = cars_img[:-4]
                image_dict[key] = pygame.image.load(path).convert_alpha()

        # Loop responsible for render car images and pilot names after execution 
        # and graphically demonstrates selection of Genetic Algorithm backend code.
        for i in range(0, len(individual)):

            x += 51
            z -= 8

            if individual[i] == 1:
                screen.blit(image_dict['Car' + str(i)], (x, position_y - z))
                screen.blit(font.render(pilot_names_list[i], False, (255, 255, 255)), (x, position_y - z * 1.2))
            else:
                screen.blit(image_dict['Car' + str(i)], (x, y))
            pygame.display.update()
            clock.tick(60)
                
        # Pygame function to exit Genetic Cars Demonstration.
        exit_genetic_cars(render_buttons_dict["back_menu"], render_buttons_dict["close_menu"])
   
    
# Function responsible for defining the values ​​referring
# to the attributes of the pilot, 
# each condition assigns and simulate a different level of difficulty.
def difficulty_selection(selected: Tuple, value_selection: Any) -> None:
    
    # Constants defined as global, their values ​​do not change during execution.
    global initial_value
    global final_value
    global level
    global limit
      

    # Conditional that selects difficulty level of demonstration.
    if value_selection == 1:
        initial_value = 99
        final_value = 120
        level = "Easy Difficulty - "
        limit = 1.5

    elif value_selection == 2:
        initial_value = 128.00
        final_value = 161.00
        level = "Normal Difficulty - "
        limit = 1.5

    else:
        initial_value = 170.00
        final_value = 200.00
        level = "Hard Difficulty - "
        limit = 1.5


    
def credits():
    
    rendering_menu_images('Menu/credit_screen.png')
    exit_genetic_cars(render_buttons_dict["back_menu"], render_buttons_dict["close_menu"])
   
   
def instructions():

    rendering_menu_images('Menu/instructions_screen.png')
    exit_genetic_cars(render_buttons_dict["back_menu"], render_buttons_dict["close_menu"])
   
def results():

    count = 0
    color = (0,0,0)
    screen = pygame.display.set_mode((1280, 720))
    rendering_menu_images('Menu/results_screen.png')


    # Render the results of the execution of genetic algorithms inside Pygame Results Screen in menu.
    with open("results/output.txt", 'r') as results:

            for line in results:
                line = line.strip()
                count += 2
                screen.blit((pygame.font.SysFont('Arial',18, True, True).render(line, True, color)),(300,8*count+180))
            count = 0
            
    pygame.display.update()
    
    exit_genetic_cars(render_buttons_dict["back_menu"], render_buttons_dict["close_menu"])

    
def exit_genetic_cars(back_menu, close_menu):
    
    # Close Genetic Cars demonstration.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if back_menu.collidepoint(mouse_pos):
                    menu.mainloop(surface)

                elif close_menu.collidepoint(mouse_pos):
                        print('Genetic Cars Demonstration Was Closed')
                        pygame.quit()
                        sys.exit()
                        
   
# Pygame-Menu, generates an interactive menu for project Genetic Cars.
menu = pygame_menu.Menu(
    height=720,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Genetic Cars',
    width=1280
)

menu.add.selector('Difficulty Level: ', [('Normal', 2), ('Hard', 3), ('Easy', 1)],
                default=int(2), onchange=difficulty_selection,
                margin=(10, 15), font_size=35)

menu.add.button('Start Demonstration',
                start_demonstration, margin=(10, 15), font_size=35)

menu.add.button('Credits',
                credits, margin=(10, 15), font_size=35)

menu.add.button('Instructions',
                instructions,
                margin=(10, 15), font_size=35)

menu.add.button('Last Run Results',
                results, margin=(10, 15), font_size=35)

menu.add.button('Exit',
                pygame_menu.events.EXIT, margin=(10, 15), font_size=35)

if __name__ == '__main__':
    menu.mainloop(surface)

import genetic_cars