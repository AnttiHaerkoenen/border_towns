import os
import re
from pathlib import Path
from typing import Callable, Union, Generator
import logging

import pandas as pd
from pandas import DataFrame
import click


def text_file_generator(
        data_path: Path,
        rule: str,
) -> Generator:
    if not data_path.exists():
        raise FileNotFoundError(f"Specified data path {data_path} does not exist.")

    paths = list(data_path.rglob(rule))
    pages = ['_'.join(re.findall(r'\d+', path.name)) for path in paths]

    for path, page in sorted(zip(paths, pages), key=lambda x: x[1]):
        text = path.read_text()
        yield path, page, text


def read_word_list(file):
    data = pd.read_csv(str(file), header=None)
    data.columns = 'word regex'.split()
    data.dropna(inplace=True)
    data.sort_values(by='word', inplace=True)
    words = data['word']
    regex = data['regex']
    return {w.casefold(): r for w, r in zip(words, regex)}


def get_kwic(
        file: Path,
        regex_dict: dict,
        page: int,
        window_size: int,
):
    rows = []
    logging.info(f'Processing file {file.name}')
    text = file.read_text()
    for w, r in regex_dict.items():
        matches = r.finditer(text)
        for m in matches:
            start, end = m.span()
            start = start - window_size
            if start < 0:
                start = 0
            end = end + window_size
            if end >= len(text):
                end = len(text) - 1
            context = text[start:end].replace('\n', ' ')
            row = {
                'file': file.stem,
                'page': page,
                'keyword': w,
                'context': context,
            }

            rows.append(row)

    return pd.DataFrame(rows).sort_values('keyword')


def get_kwic_for_word(
        *,
        data_path: Path,
        rule: str,
        term: str,
        regex: re.Pattern,
        window_size: int,
        size_limit: int,
) -> DataFrame:
    texts = text_file_generator(data_path, rule)
    logging.info(f'Searching {data_path} for {term}')
    rows = []

    for file, page, text in texts:
        if len(rows) >= size_limit:
            break
        matches = regex.finditer(text)

        for m in matches:
            start, end = m.span()
            start = start - window_size
            if start < 0:
                start = 0
            end = end + window_size
            if end >= len(text):
                end = len(text) - 1
            context = text[start:end].replace('\n', ' ')
            row = {
                'file': file.stem,
                'page': page,
                'keyword': term,
                'context': context,
            }
            rows.append(row)

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame.from_records(rows).sort_values('page').head(size_limit).reset_index()


def save_kwic_by_word(
        *,
        input_dir: Path,
        output_dir: Path,
        rule: str,
        wordlist: Path,
        redo_search: bool,
        window_size: int,
        size_limit: int,
        word_filter_rule: Union[str, Callable[[str], bool]],
):
    output_dir.mkdir(parents=True, exist_ok=True)
    words = read_word_list(wordlist)
    regex = {
        word: re.compile(regexpr, flags=re.IGNORECASE)
        for word, regexpr
        in words.items()
    }

    for term, regex in regex.items():
        if word_filter_rule != 'all' and not word_filter_rule(term):
            continue
        output_file = output_dir / f"{term.replace(' ', '_')}.csv"
        if output_file.is_file() and not redo_search:
            logging.info(f"{output_file} exists, skipping {term}")
            continue
        kwic_term = get_kwic_for_word(
            data_path=input_dir,
            rule=rule,
            term=term,
            regex=regex,
            window_size=window_size,
            size_limit=size_limit,
        )
        if not kwic_term.empty:
            kwic_term.drop(columns=['index', 'keyword', 'page'], inplace=True)
        logging.info(f'Saving data: {term}')
        kwic_term.to_csv(output_file)


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
@click.argument('wordlist_filepath', type=click.Path(exists=True))
@click.option('--window_size', type=click.IntRange(1, 1000), default=50, help='size of context window, characters, both directions')
@click.option('--size_limit', type=click.IntRange(10, 50_000), default=1000, help='maximum number of results saved in file')
@click.option('--files', type=click.STRING, default='*.txt', help='rule to select suitable files [*.txt]')
@click.option('--redo', type=click.BOOL, default=True, help='whether or not to re-search existing files [True]')
def main(
    input_filepath, 
    output_filepath, 
    wordlist_filepath,
    window_size,
    size_limit,
    files,
    redo,
    ):
    """
    Performs keywords-in-context analysis and saves results in csv files
    """
    logger = logging.getLogger(__name__)
    input_dir = Path(input_filepath)
    output_dir = Path(output_filepath)
    wordlist = Path(wordlist_filepath)

    save_kwic_by_word(
        output_dir=output_dir,
        input_dir=input_dir,
        rule=files,
        wordlist=wordlist,
        redo_search=redo,
        window_size=window_size,
        size_limit=size_limit,
        word_filter_rule='all',
    )
    logger.info(f'Keywords saved to {output_dir}')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file = Path('./logs') / Path(__file__).stem
    logging.basicConfig(filename=log_file, level=logging.INFO, format=log_fmt)

    main()
