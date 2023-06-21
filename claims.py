"""
This module provides functions for parsing the config file

"""
from random_variables import r_poisson, r_pareto # pylint: disable=import-error

distribution_map = {'Poisson': r_poisson,
                    'Pareto': r_pareto}


def generate_claims(size: int,
                    frequency: dict[callable, dict[float]],
                    severity: dict[callable, dict[float]],
                    development_pattern: list[float]) -> list[dict[list]]:
    """
    Generate simulated claims based on provided parameters.

    Args:
        size (int): The number of simulations/claims to generate.
        frequency (dict[callable, dict[float]]): A dictionary specifying the frequency distribution
            and its parameters.
        severity (dict[callable, dict[float]]): A dictionary specifying the severity distribution
            and its parameters.
        development_pattern (list[float]): A list of development pattern coefficients.

    Returns:
        list[dict[list]]: A list of dictionaries representing the generated claims. Each dictionary
            contains the following keys: 'simId', 'claimId', 'claimDevelopmentYear',
            and 'claimAmount'.

    """
    claims = [{'simId': [],
               'claimId': [],
               'claimDevelopmentYear': [],
               'claimAmount': []} for _ in development_pattern]

    for sim in range(size):
        nb_claims = frequency['distribution'](**frequency['parameters'])
        if nb_claims == 0:
            for development_year, development_coefficient in enumerate(development_pattern):
                claims[development_year]['simId'] += [sim]
                claims[development_year]['claimId'] += [0]
                claims[development_year]['claimDevelopmentYear'] += [development_year]
                claims[development_year]['claimAmount'] += [0]
                continue

        for claim_id in range(nb_claims):
            ultimate_claim_amount = severity['distribution'](
                **severity['parameters'])
            development_factor = 0.0
            for development_year, development_coefficient in enumerate(development_pattern):
                development_factor += development_coefficient
                claims[development_year]['simId'] += [sim]
                claims[development_year]['claimId'] += [claim_id]
                claims[development_year]['claimDevelopmentYear'] += [development_year]
                claims[development_year]['claimAmount'] += [
                    ultimate_claim_amount * development_factor]
    return claims
