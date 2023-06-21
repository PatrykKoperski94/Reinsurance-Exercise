# Introduction:
In this exercise, the objective is to price four excess of loss (xs) treaties with varying parameters. The pricing program needs to provide several key statistics related to losses exceeding the deductible. These statistics include:

1. Average Loss: This represents the average value of losses that exceed the deductible for each development year.

2. VaR(99%): VaR stands for Value at Risk and represents the threshold level of losses that have a 99% probability of not being exceeded. It provides an estimate of the potential maximum loss beyond the deductible.

3. TVaR(99%): TVaR, also known as Tail Value at Risk, goes beyond VaR by considering the average value of losses beyond the VaR threshold. It provides a measure of the potential magnitude of extreme losses.

4. Premium: The premium is calculated using the formula: Premium = Average Loss - (TVaR(99%) - Average Loss) * Cost of Capital. It represents the amount charged to the reinsured company for the excess of loss coverage.

5. Average Payment Pattern: This metric calculates the average percentage of the loss incurred claims by the reinsurer for a given development year. Only claims with strictly positive recoveries are considered in computing the average payment pattern.

The pricing program offers flexibility as it allows for pricing multiple treaties simultaneously and accommodating different development year horizons. 
Moreover, it establishes a foundation for incorporating additional frequency and severity distributions in the future, enabling more comprehensive and adaptable pricing capabilities.

# Config
I've run the simulation using the following config values:
```Yaml
simulations:
  nb: 1_000_000
  seed: 0

  frequency:
    distribution: "Poisson"
    parameters:
      rate: 1

  severity:
    distribution: "Pareto"
    parameters:
      shape: 1.2
      scale: 2_000_000

  development_pattern: [0.3, 0.6, 0.1]

financials:
  cost_of_capital: 0.08

treaties:
  - name: 10m xs 5m
    type: xs
    parameters:
      deductible: 5_000_000
      limit: 10_000_000
      aad: 0
      aal: 0

  - name: 10m xs 5m, AAD 2m
    type: xs
    parameters:
      deductible: 5_000_000
      limit: 10_000_000
      aad: 2_000_000
      aal: 0

  - name: 10m xs 5m, AAL 12m
    type: xs
    parameters:
      deductible: 5_000_000
      limit: 10_000_000
      aad: 0
      aal: 12_000_000   

  - name: 10m xs 5m, AAD 2m, AAL 12m
    type: xs
    parameters:
      deductible: 5_000_000
      limit: 10_000_000
      aad: 2_000_000
      aal: 12_000_000          
```
# Results
| Statistics                  | Development Year |               |               |
|-----------------------------|------------------|---------------|---------------|
| **Treaties**                | **0**            | **1**         | **2**         |
| **average_loss**            |                  |               |               |
| 10m xs 5m                   | 385,590.55       | 1,444,493.94  | 1,639,271.79  |
| 10m xs 5m, AAD 2m           | 299,791.52       | 1,149,415.44  | 1,309,416.80  |
| 10m xs 5m, AAL 12m          | 381,808.42       | 1,389,114.11  | 1,567,564.18  |
| 10m xs 5m, AAD 2m, AAL 12m  | 296,760.45       | 1,104,012.83  | 1,250,638.67  |
| **VaR**                     |                  |               |               |
| 10m xs 5m                   | 10,000,000.00    | 13,109,982.96 | 14,451,779.85 |
| 10m xs 5m, AAD 2m           | 10,000,000.00    | 11,965,095.74 | 13,300,921.08 |
| 10m xs 5m, AAL 12m          | 10,000,000.00    | 12,000,000.00 | 12,000,000.00 |
| 10m xs 5m, AAD 2m, AAL 12m  | 10,000,000.00    | 11,965,095.74 | 12,000,000.00 |
| **TVaR**                    |                  |               |               |
| 10m xs 5m                   | 10,299,190.02    | 17,398,102.94 | 18,503,574.03 |
| 10m xs 5m, AAD 2m           | 10,272,148.11    | 16,540,159.68 | 17,710,277.37 |
| 10m xs 5m, AAL 12m          | 10,119,080.20    | 12,000,000.00 | 12,000,000.00 |
| 10m xs 5m, AAD 2m, AAL 12m  | 10,104,851.90    | 11,999,898.92 | 12,000,000.00 |
| **premium**                 |                  |               |               |
| 10m xs 5m                   | 1,178,678.50     | 2,720,782.66  | 2,988,415.97  |
| 10m xs 5m, AAD 2m           | 1,097,580.05     | 2,380,674.98  | 2,621,485.65  |
| 10m xs 5m, AAL 12m          | 1,160,790.16     | 2,237,984.98  | 2,402,159.05  |
| 10m xs 5m, AAD 2m, AAL 12m  | 1,081,407.76     | 1,975,683.72  | 2,110,587.58  |
| **average_payment_pattern** |                  |               |               |
| 10m xs 5m                   | 4.22%            | 34.86%        | 60.91%        |
| 10m xs 5m, AAD 2m           | 4.57%            | 34.64%        | 60.79%        |
| 10m xs 5m, AAL 12m          | 4.60%            | 34.98%        | 60.42%        |
| 10m xs 5m, AAD 2m, AAL 12m  | 4.96%            | 34.80%        | 60.24%        |

*Note: loss amounts are cumulative w.r.t. development years. The column `Development Year ==2` represents losses at ultimate.*

# Interpretation
Assumption: all contracts have unlimited free reinstatements.

Average Loss: 
- `10m xs 5m`: exhibits the highest  (`1,639,271.79`) average loss in the final development year. This is expected as there are no limits on consecutive claims covered.
- `10m xs 5m, AAD 2m`: the insurer bears a 2m annual aggregate deductible, resulting in a significantly lower average loss of `1,309,416.80` compared to the previous case.
- `10m xs 5m, AAL 12m`: caps the annual intervervention of the reinsurer to `12m`. It has a slightly lower average loss than the case without the aal. This is mainly driven by the fact that there is on average 1 claim per year and the aal activates on the second claim in the year.
- `10m xs 5m, AAD 2m, AAL 12m`: combines both an aad and an aal. This is the contract with the lowest average loss (`1,250,638.67`).

VaR:
All treaties have a VaR(99%) in the first development year of `10m`. This is due to the fact that recoveries are limited to `10m` per occurrence thus this seems to be the most frequent value in the 99th percentile of losses.
- `10m xs 5m`: Again, this contract exhibits the most extreme numbers in development year 1 and year 2 because recoveries are uncapped and there is no delay in reinsurer's intervention via an aad.
- `10m xs 5m, AAD 2m`: The aad lowers the VaR both in development year 1 and year 2.
- `10m xs 5m, AAL 12m`: Recoveries are capped to `12m` because of the aal.
- `10m xs 5m, AAD 2m, AAL 12m`: Recoveries are capped to `12m` because of the aal. But we have a lower VaR(99%) in development year 1 thanks to the aad.

TVaR:
The conclusions are similar to the VaR case but we can better identify the true benefit of an AAL.
- `10m xs 5m`: The average losses above the 99th percentile amount to `18,503,574.03`, way above the average loss. This suggests that the pricing formula should reflect the possible extreme scenario.
- `10m xs 5m, AAD 2m`: The aad lowers the TVaR both in development year 1 and year 2 but is way less effective than an aal.
- `10m xs 5m, AAL 12m`: Recoveries are capped to `12m` because of the aal.
- `10m xs 5m, AAD 2m, AAL 12m`: Recoveries are capped to `12m` because of the aal.

Premium:
- `10m xs 5m`: The most expensive contract because it transfers the most risk to the reinsurer
- `10m xs 5m, AAD 2m`: The aad reduces the exposure of the reinsurer, therefore it is less expensive that the contract above. We've seen that the aad reduces the recoveries quite significantly, it is still not as effective as an aal.
- `10m xs 5m, AAL 12m`: The aal is responsible for a +-$500k reduction in premium w.r.t. `10m xs 5m` thanks to its annual aggregate recoveries capping capabilities.
- `10m xs 5m, AAD 2m, AAL 12m`: The least expensive contract in terms of premium but a sizeable part of the risk remains at the insurer.

Average Payment Pattern:

The 'From Ground Up' payment pattern is `[0.3, 0.6, 0.1]` meaning that only `30%` of loss amounts are incurred in the first development year. Given a deductible of `5m` accross the board we notice that the average payment coefficient for the reinsurer does not exceed `5%` in the first year.
Then, `90%` (`0.3+0.6`) of the total claim amount is incurred in the second development year. The incurred claim amount of the reinsurer hovers around `35%` of its final value, it illustrates that claims start to significantly exceed the deductibles w.r.t. previous year.
Finally, the third development year exhibits the largest average payment coefficient (`+-60.5%`). It shows that, for this particular case, the reinsurer almost fully bares the burden of loss aggravation in the tails of the distribution.

Normally we'd discount the amount in development year 2 to bring it to an actualized loss today. 

Variations between contracts are similar to the ones discussed in the previous paragraphs.

