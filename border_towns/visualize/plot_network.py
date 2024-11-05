# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path

import click
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
@click.argument('query')
def main(input_filepath, output_filepath, query):
    """
    Plots a subset of a network from csv edgelist filtered by query
    """
    logger = logging.getLogger(__name__)
    input_fp = Path(input_filepath)
    output_fp = Path(output_filepath)
    logger.info('Reading and filtering data')
    data = pd.read_csv(input_fp).query(query)
    logger.info(f'{data.shape[0]} edges found')
    G = nx.from_pandas_edgelist(
        data,
        'nimi1',
        'nimi2',
        create_using=nx.MultiDiGraph,
    )
    logger.info(f'Graph contains nodes {G.degree()}')
    A = nx.nx_agraph.to_agraph(G)
    A.draw(output_fp, prog="dot")
    logger.info(f'Graph exported to {output_fp}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file = Path('./logs') / Path(__file__).stem
    logging.basicConfig(filename=log_file, level=logging.INFO, format=log_fmt)

    main()
