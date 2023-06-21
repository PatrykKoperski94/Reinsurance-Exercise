# Reinsurance-Exercise
# Claim Simulation and Treaty Analysis

This project simulates claim data and applies treaties to generate statistics based on the recoveries. It allows users to modify the values in the `config.yaml` file and perform simulations by executing the main.py file.

## Prerequisites

- Python 3.x
- Required Python packages: pandas, PyYAML

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/claim-simulation.git
   ```

2. Install the required Python packages:

   ```bash
   pip install pandas PyYAML
   ```

3. Modify the configuration

   Open the `config.yaml` file and adjust the simulation parameters and treaty settings according to your requirements.

4. Run the simulation

   Execute the `main.py` file to run the simulation and generate the statistics:

   ```bash
   python main.py
   ```

5. View the results

   The generated statistics will be displayed on the console and saved to a `statistics.csv` file.

## Configuration

The `config.yaml` file contains various parameters that can be adjusted to customize the simulations and treaty analysis. Below is a brief overview of the configuration:

- `simulations`: Parameters related to claim data simulation, including size, frequency distribution, severity distribution, and development pattern.
- `treaties`: List of treaty configurations, including type, parameters, and name.
- `financials`: Parameters related to financial calculations, such as the cost of capital.

Feel free to modify these parameters to suit your specific needs.
