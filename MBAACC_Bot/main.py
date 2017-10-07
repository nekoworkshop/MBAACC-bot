from __future__ import print_function
import time
from MBAACC_Bot.InputInjector import *
from MBAACC_Bot.processInjector import *
import os
import neat
import numpy

injector = ProcessInjector()

def main():

   run()
   while True:
      injector.stageDataPrettyPrint()
      time.sleep(0.01)

def run():
   config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        os.path.join(os.path.dirname(__file__),'config-mbaacc'))

   # Create the population, which is the top-level object for a NEAT run.
   p = neat.Population(config)

   # Add a stdout reporter to show progress in the terminal.
   p.add_reporter(neat.StdOutReporter(True))
   stats = neat.StatisticsReporter()
   p.add_reporter(stats)
   p.add_reporter(neat.Checkpointer(5))

   # Run for up to 300 generations.
   winner = p.run(eval_genomes, 30)

def eval_genomes(genomes, config):
   for genome_id, genome in genomes:

      #start evaluation of a single genome
      net = neat.nn.FeedForwardNetwork.create(genome, config)
      while True:
         if(injector.get1pHp() == 0 or injector.get2pHp() == 0):
            print("match end detected")
            break
         time.sleep(0.036)
         output = net.activate(injector.getStageData())
         #print(output)
         SendCommand(numpy.argmax(output))
      genome.fitness = ((injector.get1pHp() - injector.get2pHp() + 11400)/22800)
      print("Fitness:" + str(genome.fitness))
      while True:
         if(injector.get1pHp() != 0 and injector.get2pHp() !=0 ):
            print("match restart detected")
            break


if __name__ == "__main__": main()