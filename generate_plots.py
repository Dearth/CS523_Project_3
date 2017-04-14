from functools import wraps

import matplotlib.pyplot as plt
import numpy as np


def read_file(file_name):
    return np.genfromtxt('data/' + file_name, delimiter=',')


def read_range(file_name, interval):
    return np.stack([read_file(file_name + str(i)) for i in interval])


def from_group(fit_func, base='single_ga', num='single', output='fitness', average=True):
    data = read_range(
        '{base}/{f}/{num}_{f}_{out}_'.format(f=fit_func, base=base, num=num, out=output),
        range(1, 8))
    return np.average(data, 0)[:, 0:-1] if average else data


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
    plt.plot(biomass[0:50])


@new_fig_save(fn="fig3a", title="Two Species Evolved Growth Rates", xlabel="Iteration #", ylabel="Fitness")
def plot3a():
    biomass = np.average(from_group('biomass', base='two_ga', num='two'), axis=1)

    plt.plot(biomass[0:50])


@new_fig_save(fn="fig3b", title="Two Species Growth Rates", xlabel="Trial #", ylabel="Growth Rate (/ 100)")
def plot3b():
    biomass = from_group('biomass', base='two_ga', num='two', output='config', average=False)
    print("Two species covariance", np.cov(biomass[:,0], biomass[:,1]))
    plt.plot(biomass)


@new_fig_save(fn="fig4a", title="Biomass vs Firefighters", xlabel="Number of Firefighters", ylabel="Fitness")
def plot4a():
    biomass = np.average(np.average(read_range('firefighter_biomass/ff_biomass_fitness_', range(1, 11)), 0)[:,0:-1], axis=1)

    plt.plot(np.arange(0, len(biomass)) * 50, biomass)

plot1()
plot2a()
plot3a()
plot3b()
plot4a()
