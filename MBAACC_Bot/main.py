from __future__ import print_function
import time
from MBAACC_Bot.InputInjector import *
from MBAACC_Bot.processInjector import *
import os
import neat
import numpy
from MBAACC_Bot.visualize import *

injector = ProcessInjector()


def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)
    run()
    while True:
        injector.stageDataPrettyPrint()
        time.sleep(0.01)


def run():
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         os.path.join(os.path.dirname(__file__), 'config-mbaacc'))

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 30)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:

        # start evaluation of a single genome
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        # draw_net(config, genome, view=True, filename=str(genome_id) + "-net.gv")

        # Main simulation loop.
        # The loop ends when either character dies, then a fitness score will be calculated.
        while True:
            if (injector.get1pHp() == 0 or injector.get2pHp() == 0):
                print("match end")
                break

            # This controls the sample rate of the network
            time.sleep(0.056)

            # Read response from the network
            output = net.activate(injector.getStageData())
            #print(output)

            SendCommand(numpy.argmax(output))

    # Calculate fitness based on the match result.
    genome.fitness = ((injector.get1pHp() - injector.get2pHp() + 11400) / 22800)
    print("Fitness:" + str(genome.fitness))

    # Waiting room. Loop until the match is reset and started.
    while True:
        if (injector.get1pHp() != 0 and injector.get2pHp() != 0):
            print("match start")
            break


if __name__ == "__main__": main()
