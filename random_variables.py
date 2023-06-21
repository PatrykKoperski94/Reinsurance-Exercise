"""
This module provides functions for generating random numbers from different probability
distributions.

The available functions are:
- r_pareto(shape, scale): Generate a random number from the Pareto distribution.
- r_exponential(rate): Generate a random number from the exponential distribution.
- r_poisson(rate, interval_length=1): Generate a random number from the Poisson distribution.

The module utilizes the 'random' and 'math' modules from the Python standard library.

"""
import math
import random

def r_pareto(shape, scale) -> float:
    """
    Generate a random number from the Pareto distribution.

    Args:
        shape (float): The shape parameter of the Pareto distribution.
        scale (float): The scale parameter of the Pareto distribution.

    Returns:
        float: A random number from the Pareto distribution.
    """
    # The hint suggests using r_pareto = scale/(1-r_uniform)**(1/shape),
    # but it is better to limit the number of divisions to improve computational accuracy,
    # so we can write it as scale * (1 - random.uniform(0, 1)) ** (-1 / shape).
    return scale * (1 - random.uniform(0, 1)) ** (-1 / shape)

def r_exponential(rate) -> float:
    """
    Generate a random number from the exponential distribution.

    Args:
        rate (float): The rate parameter of the exponential distribution.

    Returns:
        float: A random number from the exponential distribution.
    """
    return -math.log(1 - random.uniform(0, 1)) / rate

def r_poisson(rate, interval_length=1) -> int:
    """
    Generate a random number from the Poisson distribution.

    Args:
        rate (float): The rate parameter of the Poisson distribution.
        interval_length (float, optional): The length of the interval. Defaults to 1.

    Returns:
        int: A random number from the Poisson distribution.
    """
    # The time between two Poisson-distributed events has an exponential distribution with
    # mean_exponential = 1 / mean_poisson. We stop when the event occurs outside the interval.
    total_occurrences = 0
    time_of_occurrence = 0.0
    while time_of_occurrence <= interval_length:
        time_of_occurrence += r_exponential(rate)
        if time_of_occurrence <= interval_length:
            total_occurrences += 1

    return total_occurrences
