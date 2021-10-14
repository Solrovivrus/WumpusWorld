from wumpusWorld import wumpusWorld
from problemGenerator import problemGenerator
# from simpleExplorer import simpleExplorer
from reasonedExplorer import reasonedExplorer
from termcolor import cprint
from pyfiglet import figlet_format
import sys
from colorama import init
init(strip=not sys.stdout.isatty()) 


worlds = wumpusWorld
problem = problemGenerator
rea = reasonedExplorer
# simple = simpleExplorer

cprint(figlet_format('WUMPUS WORLD', font='letters'),
       'white', 'on_blue', attrs=['bold', 'blink'])

print("Hello! And welcome to the wumpus world. We are going to start by setting up our caves.")
print("First, give us the probability in which you'd like to encounter pits and wumpi in the caves.")

# getting caves initialized of random sizes 
caves = worlds.worldGenerator()

# inputs for probability of encountering an obstacle
pits = input("Probability (0-.9) of generating a pit: ")
whatsLeft = .9 - float(pits)
wumpi = input("Probability (0-" + str(whatsLeft) + ") of generating a wumpi: ")
# added one for blocks, just uses whatever probability left to make obstacles
whatsLeft = whatsLeft - float(wumpi)
blocks = input("Probability (0-" + str(whatsLeft) + ") of generating an obstacle: ")

# sends the caves and desired probabilities to generate the worlds appropriately
caves = problem.generateWorld(caves, wumpi, pits, blocks)

# simple.placeExplorer(caves[1])

rea.placeExplorer(caves[0])

