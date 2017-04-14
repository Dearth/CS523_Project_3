from functools import wraps
from random import random
import numpy as np

import matplotlib.pyplot as plt


def read_file(file_name):
    return np.genfromtxt('data/' + file_name, delimiter=',')


def read_range(file_name, interval):
    return np.stack([read_file(file_name + str(i)) for i in interval])

def save(file_name):
    plt.savefig(filename="results/" + file_name, frameon=True, dpi=200)


# Return p_m and the convergence history
def run_ga():
    return list(range(0, 100, 1))


def new_fig_save(fn, title, xlabel, ylabel):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            plt.figure()
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)

            func(*args, **kwargs)

            plt.ylim(0, 5500)
            plt.autoscale(enable=True, axis='x', tight=True)
            save(fn)

        return wrapper

    return decorator


@new_fig_save(fn="fig1", title="Biomass vs Longevity", xlabel="Biomass (%)", ylabel="Longevity (steps)")
def plot1():
    readin = lambda par: np.average(read_range('single_ga/{0}/single_{0}_fitness_'.format(par), range(1, 8)), 0).flat
    biomass = readin('biomass')
    longevity = readin('longevity')
    # data/single_ga/longevity/single_longevity_config_8 is empty

    ordered = np.argsort(biomass)
    plt.plot(biomass[ordered], longevity[ordered])


@new_fig_save(fn="fig2a", title="Biomass based Fitness Convergence", xlabel="Iteration #", ylabel="Fitness")
def plot2a():
    history = run_ga()
    plt.plot(history)


@new_fig_save(fn="fig2b", title="Longevity based Fitness Convergence", xlabel="Iteration #", ylabel="Fitness")
def plot2b():
    history = run_ga()
    plt.plot(history)


@new_fig_save(fn="fig3a", title="Biomass Fitness Landscape", xlabel="Biomass", ylabel="Fitness")
def plot2a():
    history = run_ga()
    plt.plot(history)


plot1()
plot2a()
plot2b()
