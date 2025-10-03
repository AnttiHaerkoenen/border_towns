# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path

import click
from trogon import tui
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


@tui()
@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
@click.argument('source')
@click.argument('target')
@click.argument('query')
def main(input_filepath, output_filepath, source, target, query):
    """
    Plots a network from a csv edgelist filtered by query
    """
    logger = logging.getLogger(__name__)
    input_fp = Path(input_filepath)
    output_fp = Path(output_filepath)

    logger.info('Reading and filtering data')
    edge_data = pd.read_csv(input_fp).query(query)
    logger.info(f'{edge_data.shape[0]} edges from {source} to {target} found')

    G = nx.from_pandas_edgelist(
        edge_data,
        source,
        target,
        edge_attr=True,
        create_using=nx.MultiDiGraph,
    )

    logger.debug(f'Graph contains nodes {G.degree()}')
    A = nx.nx_agraph.to_agraph(G)
    color_mapper = {
        '1100': 'red',
        '1200': 'black',
        '1300': 'blue',
        '2013': 'purple',
        '2014': 'green',
        '5002': 'yellow',
    }

    for row in edge_data.itertuples():
        if row.nimi_source not in A:
            continue
        A.get_node(row.nimi_source).attr['color'] = color_mapper.get(row.paikkatunnus_source, 'black')

    A.draw(output_fp, prog='dot')
    logger.info(f'Graph exported to {output_fp}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file = Path('./logs') / Path(__file__).stem
    logging.basicConfig(filename=log_file, level=logging.INFO, format=log_fmt)

    main()
