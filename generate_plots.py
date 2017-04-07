from functools import wraps
from random import random

import matplotlib.pyplot as plt


def save(file_name):
    plt.savefig(filename="results/" + file_name, frameon=True, dpi=200)


def evaluate(p):
    return random() * 1, random() * 100, random() * 10


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


plot1(list(range(0, 10, 1)))
