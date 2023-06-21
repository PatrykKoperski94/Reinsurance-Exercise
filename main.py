"""
Simulate claim data and apply treaties to generate statistics.

This module simulates claim data based on the provided configuration,
applies treaties to the claims,
and generates statistics based on the treaty recoveries.

The module relies on the following external modules:
- random: for setting the seed for simulations.
- pandas: for data manipulation and analysis.
- config: for accessing the configuration parameters.
- claims: for the generate_claims function used for claim data simulation.

The main functionality includes:
- Setting pandas display options for better visualization of data.
- Defining the apply_treaty function to apply treaties to claims.
- Simulating claim data using the generate_claims function.
- Applying treaties to the generated claims and storing the results.
- Calculating various statistics based on the treaty recoveries.
- Exporting the statistics to a CSV file.

"""

import random
import pandas as pd
from config import config  # pylint: disable=import-error
from claims import generate_claims  # pylint: disable=import-error


# Permanently changes the pandas settings
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.float_format", lambda x: "{:,.0f}".format(x))  # pylint: disable=consider-using-f-string unnecessary-lambda


def apply_treaty(claims, treaty):  # pylint: disable=redefined-outer-name
    """
    Apply a treaty to the provided claims data.

    The function calculates treaty recoveries for each claim based on the
    provided treaty parameters.

    Args:
        claims (dict): The claims data containing 'claimId' and 'claimAmount' information.
        treaty (object): The treaty object representing the specific treaty type and its parameters.

    Returns:
        dict: The modified claims data with the addition of 'treatyRecoveries' information.

    """
    claims["treatyRecoveries"] = []
    for claim_id, claim_amount in zip(claims["claimId"], claims["claimAmount"]):
        if claim_id == 0:
            treaty_year = treaty["type"](**treaty["parameters"])
        treaty_year = treaty_year.apply_treaty(claim_amount)
        claims["treatyRecoveries"] += [treaty_year.recoveries]
    return claims


if __name__ == "__main__":
    random.seed(config["simulations"]["seed"])

    claims = generate_claims(
        size=config["simulations"]["nb"],
        frequency=config["simulations"]["frequency"],
        severity=config["simulations"]["severity"],
        development_pattern=config["simulations"]["development_pattern"],
    )

    treaties = config["treaties"]
    results = pd.DataFrame()
    for development_year in range(len(config["simulations"]["development_pattern"])):
        for treaty in treaties:
            result = pd.DataFrame.from_dict(
                apply_treaty(claims[development_year], treaty))
            result["treatyName"] = treaty["name"]
            results = pd.concat([results, result], ignore_index=True)

    results = results.sort_values(
        by=["treatyName", "simId", "claimId", "claimDevelopmentYear"]
    ).reset_index(drop=True)

    # Statistics:
    recoveries_per_year = (
        results.groupby(["treatyName", "simId", "claimDevelopmentYear"])[
            "treatyRecoveries"]
        .sum()
        .reset_index()
    )

    average_loss = (
        recoveries_per_year.groupby(["treatyName", "claimDevelopmentYear"])[
            "treatyRecoveries"
        ]
        .mean()
        .unstack()
    )

    VaR = (
        recoveries_per_year.groupby(["treatyName", "claimDevelopmentYear"])[
            "treatyRecoveries"
        ]
        .quantile(0.99)
        .unstack()
    )

    TVaR = (
        recoveries_per_year[
            recoveries_per_year["treatyRecoveries"]
            >= recoveries_per_year.groupby(["treatyName", "claimDevelopmentYear"])[
                "treatyRecoveries"
            ].transform(lambda x: x.quantile(0.99))
        ]
        .groupby(["treatyName", "claimDevelopmentYear"])["treatyRecoveries"]
        .mean()
        .unstack()
    )

    premium = average_loss + (TVaR - average_loss) * \
        config['financials']['cost_of_capital']

    pd.set_option("display.float_format", lambda x: "{:,.3f}".format(x))  # pylint: disable=consider-using-f-string unnecessary-lambda

    results["payment_pattern"] = results["treatyRecoveries"] / results.groupby(
        ["treatyName", "simId", "claimId"]
    )["treatyRecoveries"].transform("sum")

    results["incurred"] = (
        results.groupby(["treatyName", "simId", "claimId"])["treatyRecoveries"]
        .transform("sum")
        .astype(bool)
    )

    average_payment_pattern = (results[results["incurred"]]
                               .groupby(["treatyName", "claimDevelopmentYear"])["payment_pattern"]
                               .mean()
                               .unstack()
                               )

    # Exports:
    average_loss['statistic'] = 'average_loss'
    VaR['statistic'] = 'VaR'
    TVaR['statistic'] = 'TVaR'
    premium['statistic'] = 'premium'
    average_payment_pattern['statistic'] = 'average_payment_pattern'

    statistics = pd.concat([average_loss, VaR, TVaR, premium, average_payment_pattern]).reset_index(
    ).melt(id_vars=['treatyName', 'statistic'], var_name='claimDevelopmentYear', value_name='value')
    statistics = statistics[['treatyName', 'statistic'] + [
        col for col in statistics.columns if col not in ['treatyName', 'statistic']]]

    print(statistics)
    statistics.to_csv('statistics.csv', index=False)
