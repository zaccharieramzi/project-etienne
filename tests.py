from pathlib import Path

import click

from data_summary import summarize_data


@click.command()
@click.option('visits_filename', '--data-file', type=click.Path(exists=True, dir_okay=False))
@click.option('configs_path', '--cfg', type=click.Path(exists=True, file_okay=False))
def test_all_configs(visits_filename, configs_path):
    configs_path = Path(configs_path)
    config_files = configs_path.glob('*.xlsx')
    for config_file in config_files:
        results_file = configs_path / f'results_{config_file.name}'
        summarize_data(visits_filename, config_file, results_file)


if __name__ == '__main__':
    test_all_configs()
