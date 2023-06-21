"""
This module reads a configuration file, performs mappings for distributions and treaties,
and prints the resulting configuration.

It relies on the following external modules:
- yaml: for reading the configuration file in YAML format.
- claims: for the distribution_map used for mapping distribution names.
- reinsurance: for the treaties_map used for mapping treaty types.

The main functionality includes:
- Reading the configuration file.
- Performing mappings for frequency and severity distributions.
- Performing mappings for treaty types.
- Printing the resulting configuration.

"""

import yaml
from claims import distribution_map # pylint: disable=import-error
from reinsurance import treaties_map # pylint: disable=import-error
with open('config.yaml', 'r', encoding='UTF-8') as file:
    try:
        config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        print(exc)

config['simulations']['frequency']['distribution'] = distribution_map[config['simulations']
                                                                      ['frequency']['distribution']]
config['simulations']['severity']['distribution'] = distribution_map[config['simulations']
                                                                     ['severity']['distribution']]
for index, treaty in enumerate(config['treaties']):
    config['treaties'][index]['type'] = treaties_map[config['treaties'][index]['type']]

if __name__ == '__main__':
    print(config)
