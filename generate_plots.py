from functools import wraps
from random import random

import matplotlib.pyplot as plt


def save(file_name):
    plt.savefig(filename="results/" + file_name, frameon=True, dpi=200)


def evaluate(p):
    return random() * 1, random() * 100, random() * 10


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

            save(fn)

        return wrapper

    return decorator


@new_fig_save(fn="fig1", title="Biomass vs Longevity", xlabel="Biomass (%)", ylabel="Longevity (steps)")
def plot1(p_vals):
    biomass, longevity, fitness = zip(*map(evaluate, p_vals))
    plt.plot(biomass, longevity)


@new_fig_save(fn="fig2a", title="Biomass based Fitness Convergence", xlabel="Iteration #", ylabel="Fitness")
def plot2a():
    history = run_ga()
    plt.plot(history)


@new_fig_save(fn="fig2b", title="Longevity based Fitness Convergence", xlabel="Iteration #", ylabel="Fitness")
def plot2b():
    history = run_ga()
    plt.plot(history)


plot1(list(range(0, 10, 1)))
plot2a()
plot2b()
