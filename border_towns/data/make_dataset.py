# -*- coding: utf-8 -*-
import logging
from pathlib import Path

import click
import geopandas as gpd


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path(exists=True))
def main(input_filepath, output_filepath):
    """
    """
    logger = logging.getLogger(__name__)
    logger.info("Making interim data set from raw data")

    logger.info(f"Saving data to ...")

    # TODO


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
