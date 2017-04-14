from functools import wraps

import matplotlib.pyplot as plt
import numpy as np


def read_file(file_name):
    return np.genfromtxt('data/' + file_name, delimiter=',', usecols=list(range(0,40)))


def read_range(file_name, interval):
    return np.stack([read_file(file_name + str(i)) for i in interval])


def from_group(par='biomass', base='single_ga'):
    return np.average(read_range('{base}/{0}/single_{0}_fitness_'.format(par, base=base), range(1, 8)), 0)


def save(file_name):
    plt.savefig(filename="results/" + file_name, frameon=True, dpi=300)


def new_fig_save(fn, title, xlabel, ylabel):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            plt.figure()
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)

            func(*args, **kwargs)

            plt.autoscale(enable=True, axis='x', tight=True)
            save(fn)

        return wrapper

    return decorator


@new_fig_save(fn="fig1", title="Biomass vs Longevity", xlabel="Biomass (%)", ylabel="Longevity (steps)")
def plot1():
    biomass = from_group('biomass').flat
    longevity = from_group('longevity').flat
    # data/single_ga/longevity/single_longevity_config_8 is empty

    ordered = np.argsort(biomass)
    plt.plot(biomass[ordered], longevity[ordered])
    plt.ylim(0, 5500)


@new_fig_save(fn="fig2a", title="Biomass based Fitness Convergence", xlabel="Iteration #", ylabel="Fitness")
def plot2a():
    biomass = np.average(from_group('biomass'), axis=1)
    plt.plot(biomass)


@new_fig_save(fn="fig2b", title="Longevity based Fitness Convergence", xlabel="Iteration #", ylabel="Fitness")
def plot2b():
    plt.plot()


@new_fig_save(fn="fig3a", title="Biomass Fitness Landscape", xlabel="Biomass", ylabel="Fitness")
def plot3a():
    plt.plot()


plot1()
plot2a()
plot2b()
