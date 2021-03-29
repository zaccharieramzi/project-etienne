from pathlib import Path

import click

from data_summary import summarize_data


@click.command()
@click.option('visits_filename', '--data-file', type=click.Path(exists=True, dir_okay=False))
@click.option('configs_path', '--cfg', type=click.Path(exists=True, file_okay=False))
def test_all_configs(visits_filename, configs_path):
    configs_path = Path(configs_path)
    config_files = configs_path.glob('Config_*.xlsx')
    for config_file in config_files:
        print('Config file is', config_file)
        results_file = configs_path / f'results_{config_file.name}'
        try:
            summarize_data(visits_filename, config_file, results_file)
        except ValueError:
            if 'unknown' in config_file.name:
                print('Succesfully raised error for misformed config file')
            else:
                raise
        else:
            if 'unknown' in config_file.name:
                raise ValueError('Unknown didnt break the code')


if __name__ == '__main__':
    test_all_configs()
