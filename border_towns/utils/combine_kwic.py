import os
import re
from pathlib import Path
from typing import Callable, Union, Generator
import logging
from itertools import groupby

import click
import pandas as pd


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
@click.option('--files', type=click.STRING, default='*.csv', help='rule to select suitable files [*.txt]')
def main(
    input_filepath, 
    output_filepath, 
    files,
    ):
    """
    Combines keywords-in-context analysis files with same name and saves results in csv files
    """
    logger = logging.getLogger(__name__)
    input_dir = Path(input_filepath)
    output_dir = Path(output_filepath)

    fpaths = sorted(input_dir.rglob(files), key=lambda fp: fp.stem)
    fp_grouped = {k: list(g) for k, g in groupby(fpaths, key=lambda fp: fp.stem)}

    for k, g in fp_grouped.items():
        parent_path = output_dir / g[0].parent.stem
        if not parent_path.is_dir():
            parent_path.mkdir(parents=True)
        new_path = parent_path / f'{k}.csv'

        logger.info(f"Reading data for '{k}'")
        data = [pd.read_csv(fp, index_col=0, header=0) for fp in g]
        combined_data = pd.concat(data, ignore_index=True)
        if len(combined_data) > 0:
            combined_data.to_csv(new_path)
            logger.info(f'{len(combined_data)} hits for {k}')
        else:
            logger.info(f'No hits for {k}')

    logger.info(f'Keywords saved to {output_dir}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file = Path('./logs') / Path(__file__).stem
    logging.basicConfig(filename=log_file, level=logging.INFO, format=log_fmt)

    main()
