import logging
import numpy as np
import matplotlib.pyplot as plt


import settings
from models import Robby


def evolve():
    population = np.array([Robby() for i in range(0, settings.POPULATION)])

    # data for graphs
    pop_variances = []
    min_fitnesses = []
    avg_fitnesses = []
    max_fitnesses = []
    # end of data for graphs

    for gen in range(0, settings.GENERATIONS):

        logging.info(f"Gen {gen}: {pop_fit(population)}")

        for individual in population:
            individual.live()
        logging.info(f"Generation {gen}: min: {min([r.get_fitness() for r in population])} | "
                     f"avg: {np.round(np.mean([r.get_fitness() for r in population]), 2)} | "
                     f"max: {max([r.get_fitness() for r in population])} | "
                     f"σ\u00b2: {np.var([r.get_fitness() for r in population])}")

        # data for graphs
        pop_fit_variance = np.var([r.get_fitness() for r in population])
        pop_variances.append(pop_fit_variance)
        min_fitness = min([r.get_fitness() for r in population])
        min_fitnesses.append(min_fitness)
        avg_fitness = np.round(np.mean([r.get_fitness() for r in population]), 2)
        avg_fitnesses.append(avg_fitness)
        max_fitness = max([r.get_fitness() for r in population])
        max_fitnesses.append(max_fitness)
        # end of data for graphs

        new_population = sorted(population, key=lambda organism: organism.get_fitness(),
                                   reverse=True)[:10]
        while len(new_population)<settings.POPULATION:
            mating_population = [organism for organism in population if organism.get_fitness()
                 >= np.median([r.get_fitness() for r in population])]
            parent1, parent2 = np.random.choice(
                mating_population,
                size=2,
                p=get_relative_probabilities(mating_population))
            child1, child2 = parent1.mate(parent2)

            new_population.append(child1)
            new_population.append(child2)

        population = new_population
    alpha = get_alpha(population)
    return alpha, pop_variances, min_fitnesses, avg_fitnesses, max_fitnesses


def pop_fit(population):
    pop_f_list = []
    for individual in population:
        pop_f_list.append(''.join([str(int(x)) for x in individual._dna_perception.get_sequence()]))
    return pop_f_list


def get_alpha(population):
    fittest = None
    for individual in population:
        if fittest is None:
            fittest = individual
        else:
            if fittest.get_fitness() < individual.get_fitness():
                fittest = individual
    return fittest


def get_relative_probabilities(population):
    pop_fitness = [r.get_fitness() for r in population]
    min_fitness = min(pop_fitness)
    max_fitness = max(pop_fitness)
    normalized = list(
        map(
            lambda x: normalize(x, min_fitness, max_fitness),
            pop_fitness
        )
    )
    total = sum(normalized)
    return list(map(lambda x: x/total, normalized))


def normalize(x, minf, maxf):
    return (x - minf) / (maxf - minf)

def graph(pop_vars, min_fits, avg_fits, max_fits):
    pop_variances, min_fitnesses, avg_fitnesses, max_fitnesses = pop_vars, min_fits, avg_fits, max_fits
    x = np.arange(settings.GENERATIONS)
    tickpos = [tick for tick in range(settings.GENERATIONS + 1) if tick%20==0]

    plt.subplot(2, 1, 1)
    plt.plot(x, max_fitnesses, 'green', label='Maximum fitness')
    plt.plot(x, avg_fitnesses, 'black', label='Average fitness')
    plt.plot(x, min_fitnesses, 'red', label='Minimum fitness')
    plt.xticks(tickpos, tickpos)
    plt.legend(loc='best')

    plt.subplot(2, 1, 2)
    plt.plot(x, pop_variances, 'blue', label='Fitness variance in the population')
    plt.xticks(tickpos, tickpos)
    plt.legend(loc='best')

    plt.show()


if __name__=='__main__':
    logging.basicConfig(level=20)
    alpha, pop_variances, min_fitnesses, avg_fitnesses, max_fitnesses = evolve()
    graph(pop_variances, min_fitnesses, avg_fitnesses, max_fitnesses)
    logging.info(''.join([str(int(x)) for x in alpha.get_dna_act().get_sequence()]))
    logging.info(''.join([str(int(x)) for x in alpha.get_dna_perc().get_sequence()]))
