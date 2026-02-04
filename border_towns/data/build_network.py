# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path

import click
from trogon import tui
import pandas as pd
import yaml


@tui()
@click.command()
@click.argument('node_filepath', type=click.Path(exists=True))
@click.argument('edge_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
@click.argument('node_key')
@click.argument('edge_key_1')
@click.argument('edge_key_2')
@click.argument('duplicate_filepath', type=click.Path())
@click.option('--duplicates', is_flag=True)
def main(
    edge_filepath, node_filepath, output_filepath,
    node_key, edge_key_1, edge_key_2, duplicate_filepath, duplicates
) -> 0 | 1:
    """
    Combines network data from two csv-files
    """
    logger = logging.getLogger(__name__)
    edge_fp = Path(edge_filepath)
    node_fp = Path(node_filepath)
    output_fp = Path(output_filepath)
    if duplicates:
        duplicate_fp = Path(duplicate_filepath)
    if not output_fp.exists():
        output_fp.touch()
    logger.debug('Reading data')
    edges = pd.read_csv(edge_fp, dtype='object')
    edges.drop(columns=['nimi_source', 'nimi_target'], inplace=True)
    nodes = pd.read_csv(node_fp, dtype='object')
    nodes.drop(columns=['status_alkup', 'nimen_variaatiot', 'lisatietoa'], inplace=True)

    if node_key not in nodes.columns:
        logger.error(f'{node_key} not found in {node_fp}')
        return 1
    if edge_key_1 not in edges.columns:
        logger.error(f'{edge_key_1} not found in {edge_fp}')
        return 1
    if edge_key_2 not in edges.columns:
        logger.error(f'{edge_key_2} not found in {edge_fp}')
        return 1

    network = edges.merge(nodes, right_on=node_key, left_on=edge_key_1)
    network = network.merge(nodes, right_on=node_key, left_on=edge_key_2, suffixes=['_source', '_target'])
    network.drop(columns=['hlotunnus_source', 'hlotunnus_target'], inplace=True)

    if duplicates:
        logger.info('Removing duplicates')
        duplicate_dict = yaml.load(duplicate_fp.read_text(), Loader=yaml.FullLoader)
        for k, v in duplicate_dict.items():
            for i in v:
                network.replace(
                    to_replace=str(i),
                    value=k,
                    regex=False,
                    inplace=True,
                    )
        logger.info('Duplicates removed succesfully')

    network.replace(
        to_replace='"', 
        value="'", 
        regex=True,
        inplace=True,
        )
    network.to_csv(output_fp, na_rep='NA', quotechar='"')
    logger.info(f'Network saved to {output_fp}')
    return 0


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file = Path('./logs') / Path(__file__).stem
    logging.basicConfig(filename=log_file, level=logging.INFO, format=log_fmt)

    main()
