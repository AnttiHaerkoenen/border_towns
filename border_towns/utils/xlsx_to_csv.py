# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path

import click
import pandas as pd


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
@click.option('--sheet', default=0, help='Which sheet to save in csv')
@click.option('--header', default=0, help='0 for first row, None for no header')
@click.option('--index_col', default=0, help='0 for first column, None for no index')
def main(input_filepath, output_filepath, sheet, header, index_col):
    """
    Turn xlsx-table into clean csv
    """
    logger = logging.getLogger(__name__)
    logger.info(f'Reading data from {input_filepath}')
    input_fp = Path(input_filepath)
    output_fp = Path(output_filepath)
    
    try:
        data = pd.read_excel(
            input_fp,
            sheet_name=sheet,
            header=header,
            index_col=index_col,
            dtype='object',
        )
        logger.info(f'Reading file {input_filepath} successful')
    except Exception as e:
        logger.error(f'Reading {input_filepath} failed: {e}')
    
    if data.index.dtype == 'float':
        data.set_index(data.index.values.astype(int))
        
    try:
        data.to_csv(output_fp, sep=',')
        logger.info(f'Data saved to {output_filepath}')
    except Exception as e:
        logger.error(f'Writing to {output_filepath} failed: {e}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file = Path('./logs') / Path(__file__).stem
    logging.basicConfig(filename=log_file, level=logging.INFO, format=log_fmt)

    main()
